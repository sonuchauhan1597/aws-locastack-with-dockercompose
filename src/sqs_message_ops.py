import boto3
import argparse
import create_dydb

sqs = boto3.resource('sqs',endpoint_url="http://interview-localstack:4566", region_name="ap-southeast-1")   #region_name="ap-southeast-1"
dynamodb_client = boto3.client('dynamodb', endpoint_url="http://interview-localstack:4566", region_name="ap-southeast-1") 
tablename = 'test-queue-dynamodb'
sqs_id = 'SQS_Message_ID'
sqs_msg = 'SQS_Message'


def func_consume(args):
    print(f' count: {args.count}')
    queue = sqs.get_queue_by_name(QueueName='test-queue')
    messages = queue.receive_messages(MaxNumberOfMessages=args.count[0], WaitTimeSeconds=1)

    for message in messages:
        print(f'message id: {message.message_id} \n message body: {message.body}')
        # Query if the sqs is consumed
        response = dynamodb_client.query(
            ExpressionAttributeValues={
                ':name':{
                    'S': message.message_id,
                },
            },
            KeyConditionExpression=f'{sqs_id} = :name',
            ProjectionExpression=sqs_msg,
            TableName=tablename,
        )
        # Consume if it's not consumed
        if not response['Items'] :
            response_ = dynamodb_client.put_item(
                Item={
                    sqs_id: {
                        'S': message.message_id,
                        },
                    sqs_msg: {
                        'S': message.body,
                        },
                    },
                    ReturnConsumedCapacity='TOTAL',
                    TableName=tablename,
                )
            print(response_)
        
        #delete the message once it's read or consumed from sqs
        message.delete()
        print(response)

    return

def func_show(args):
    #Show all messages from the db
    paginator = dynamodb_client.get_paginator('scan')
    for page in paginator.paginate(TableName=tablename):
        for item in page['Items']:
            print(item)

    # print("Show")

    return

def func_clear(args):
    # Delete table and create again to do it fatster
    dynamodb_client.delete_table(TableName=tablename)
    print('Table deleted')
    create_dydb.create_dynmodb_table()
    print("cleanup is complete -> Dynomod DB table is deleted and recreated")

    return

def main():
    """Parse arguments and handle request."""
    parser = argparse.ArgumentParser(description="Manage IAM Resources.")
    parser.add_argument("--new", action="store_true", default=False)
    subparsers = parser.add_subparsers(title="commands", description="valid commands")

    # Consume 
    cmd_consume = subparsers.add_parser(
        "consume", help="Consume n messages Prints n consumed messages with message content and MessageIds from SQS context"
    )
    cmd_consume.add_argument(
        "--count", type=int, nargs="+", help="count of the messages to consume", required=True
    )
    cmd_consume.set_defaults(func=func_consume)

    # Show

    cmd_show = subparsers.add_parser(
        "show", help="Show all consumed messages Prints all consumed messages with message content and MessageIds from SQS context"
    )
    cmd_show.set_defaults(func=func_show)
    # Clear
    cmd_clear = subparsers.add_parser(
        "clear", help="Clear all consumed messages from database"
    )
    cmd_clear.set_defaults(func=func_clear)

    args = parser.parse_args()

    if not hasattr(args, "func"):
        parser.error("No command specified")
    args.func(args)


if __name__ == "__main__":
    main()
