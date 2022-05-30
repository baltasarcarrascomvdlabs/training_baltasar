import json
import boto3
from boto3.dynamodb.conditions import Key

def lambda_handler(event, context):
        # TODO implementimport boto3
    
    TABLE_NAME = "Personas"
    
    # Creating the DynamoDB Client
    dynamodb_client = boto3.client('dynamodb', region_name="sa-east-1")
    
    # Creating the DynamoDB Table Resource
    dynamodb = boto3.resource('dynamodb', region_name="sa-east-1")
    table = dynamodb.Table(TABLE_NAME)
    response = table.get_item(
        Key={
            'Id': '0',
            'Edad': '22'
        }
    )
    return {
        'response' : response,
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
    
    #THE CODE FOR ACCESING DE RDS DATABASE I DID IT IN JAVA, AND I HAVE ALREADY MADE QUERIES 
    # TO RDS DB IN PYTHON, IF YOU WANT TO, I CAN ASS THAT PART TO THIS SCRIPT
    # ALSO THE KEY IS HARDCODED AS I WAS TRYING TO UNDERSTAND THE FORMAT
