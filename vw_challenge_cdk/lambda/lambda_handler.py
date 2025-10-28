import boto3
import os
import json
import uuid

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TABLE_NAME'])


def handler(event, context):

    item = {"id": str(uuid.uuid4()), **event}
    table.put_item(Item=item)
    return {
        "statusCode": 201,
        "body": json.dumps({
            "message": "Item stored",
            "id": item["id"]
        })
    }
