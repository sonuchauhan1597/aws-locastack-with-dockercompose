import boto3
import random
import create_dydb

create_dydb.create_dynmodb_table()
print(f"Created table.")

sqs = boto3.client('sqs',endpoint_url="http://interview-localstack:4566", region_name="ap-southeast-1")   #region_name="ap-southeast-1"
sqs.create_queue(QueueName='test-queue')
count = random.randint(10, 100)
while count > 0 :
    message_body="Test message {}".format(count)
    print(message_body)
    print()
    sqs.send_message(QueueUrl='http://interview-localstack:4566/000000000000/test-queue',MessageBody=message_body)
    count-=1
   
