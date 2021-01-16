# UNIR - imnavas
import os
import json

from todos import decimalencoder
import boto3
dynamodb = boto3.resource('dynamodb')
translate = boto3.client(service_name='translate',region_name='us-east-1',use_ssl=True)

def get_language(event, context):
# Copiamos metodo get 
#TODO: reutiliar funcion get
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
    result = table.get_item(
        Key={
            'id': event['pathParameters']['id']
        }
    )
    result['Item']['language']=event['pathParameters']['language']
    result_translate=translate.translate_text(Text=result['Item']['text']
                                             ,SourceLanguageCode="auto"
                                             ,TargetLanguageCode=event['pathParameters']['language'])
    result['Item']['text']=result_translate['TranslatedText']
    response = {
        "statusCode": 200,
        "body": json.dumps(result['Item'],
                           cls=decimalencoder.DecimalEncoder)
    }
    return response
"""
    result=translate.translate_text(Text="Hello,World",SourceLanguageCode="auto",TargetLanguageCode="fr")
    response = {
        "statusCode": 200,
        "body": json.dumps("[]",
                           cls=decimalencoder.DecimalEncoder)
    }
"""

def get(event, context):
    # Database obj
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    # fetch todo from the database
    result = table.get_item(
        Key={
            'id': event['pathParameters']['id']
        }
    )

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(result['Item'],
                           cls=decimalencoder.DecimalEncoder)
    }

    return response
