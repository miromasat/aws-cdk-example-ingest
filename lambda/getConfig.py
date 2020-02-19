import boto3
import os
import json
from boto3.dynamodb.conditions import Key, Attr
    
    
def main(evt, ctx):
    print('getConfig invoked')

    partition_key_name = None
    sort_key_name = None

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['TABLE_NAME'])
    if (evt['pathParameters'] is not None):
            partition_key_name = evt['pathParameters'][os.environ['PARTITION_KEY_NAME']]
     
            items = table.query(
                    KeyConditionExpression=Key(os.environ['PARTITION_KEY_NAME']).eq(partition_key_name)
            )
    else:
            items = table.scan()
        
        
    response = {
        "statusCode": 200,
        "body": json.dumps(items),  
        "isBase64Encoded":  "false",
        "headers": {}
    }    
    
    return response

