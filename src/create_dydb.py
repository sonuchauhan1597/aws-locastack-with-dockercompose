import boto3

def create_dynmodb_table():
    dynamodb = boto3.resource('dynamodb', endpoint_url="http://interview-localstack:4566", region_name="ap-southeast-1")

    table_name = 'test-queue-dynamodb'
    params = {
        'TableName': table_name,
        'KeySchema': [
            {'AttributeName': 'SQS_Message_ID', 'KeyType': 'HASH'},
            {'AttributeName': 'SQS_Message', 'KeyType': 'RANGE'}
        ],
        'AttributeDefinitions': [
            {'AttributeName': 'SQS_Message_ID', 'AttributeType': 'S'},
            {'AttributeName': 'SQS_Message', 'AttributeType': 'S'}
        ],
        'ProvisionedThroughput': {
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    }
    table = dynamodb.create_table(**params)
    print(f"Creating {table_name}...")
    table.wait_until_exists()
    return table


if __name__ == '__main__':
    db_table = create_dynmodb_table()
    print(f"Created table.")
