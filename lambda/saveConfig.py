import boto3
import os
import json
from boto3.dynamodb.conditions import Key, Attr


def main(evt, ctx):
    print('saveConfig invoked')

    partition_key_name = None
    sort_key_name = None

    if (evt['pathParameters'][os.environ['PARTITION_KEY_NAME']]):
        partition_key_name = evt['pathParameters'][os.environ['PARTITION_KEY_NAME']]

    body = json.loads(evt['body'])

    if (body[os.environ['SORT_KEY_NAME']]):
        sort_key_name = body[os.environ['SORT_KEY_NAME']]

    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['TABLE_NAME'])

    if (partition_key_name and sort_key_name):
        table.put_item(
            Item={
                os.environ['PARTITION_KEY_NAME'] : partition_key_name,
                os.environ['SORT_KEY_NAME'] : sort_key_name,
                'value' : body['value']
            }
    )

    response = {
        "statusCode": 200,
        "body": json.dumps({"status":"success", "message": "Configuration "+os.environ['SORT_KEY_NAME']+"="+body['value']+" stored"}),  
        "isBase64Encoded":  "false",
        "headers": {}
    }    
    
    return response