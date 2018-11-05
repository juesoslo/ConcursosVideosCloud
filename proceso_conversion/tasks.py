import requests
from datetime import datetime
import boto3
import os


AWS_REGION = "us-east-2"
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID", '')
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY", '')

# Create SQS client
sqs = boto3.client(
    'sqs',
    region_name=AWS_REGION,
    # Hard coded strings as credentials, not recommended.
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

queue_url = 'https://sqs.us-east-2.amazonaws.com/687383508727/cloudg7-videos-queue'

# Receive message from SQS queue
response = sqs.receive_message(
    QueueUrl=queue_url,
    AttributeNames=[
        'SentTimestamp'
    ],
    MaxNumberOfMessages=1,
    MessageAttributeNames=[
        'All'
    ],
    VisibilityTimeout=0,
    WaitTimeSeconds=0
)
print(response)

if('Messages' in response):
    message = response['Messages'][0]
    receipt_handle = message['ReceiptHandle']

    # se ejecutan las acciones de procesar video

    # URL final del aplicativo
    WEB_URL = os.environ.get("CLOUDG7_WEB_URL", '')

    # URL del servicio REST que se va a ejecutar
    url = WEB_URL+'/conversion/procesar/'

    # Se ejecuta el servicio
    response = requests.get(url) #, json=data)

    # Se imprime el resultado
    print(response.json())

    # Delete received message from queue
    sqs.delete_message(
        QueueUrl=queue_url,
        ReceiptHandle=receipt_handle
    )

    print('Received and deleted message: %s' % message)
    print("The time is %s :" % str(datetime.now()))