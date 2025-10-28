import boto3
import os
from datetime import datetime
import json

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TABLE_NAME'])
s3 = boto3.client('s3')
bucket = os.environ['BUCKET_NAME']


def handler(event, context):
    response = table.scan()
    count = len(response.get("Items", []))
    summary = {
        "timestamp": datetime.utcnow().isoformat(),
        "total_items": count
    }
    key = f"summary_{datetime.utcnow().strftime('%Y%m%d')}.json"
    s3.put_object(
        Bucket=bucket,
        Key=key,
        Body=json.dumps(summary),
        ContentType="application/json"
    )
    return {"statusCode": 200, "body": json.dumps({"summary": key})}
