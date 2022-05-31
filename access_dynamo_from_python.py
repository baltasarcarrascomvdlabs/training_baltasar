import boto3
from boto3.dynamodb.conditions import Key
from curses import is_term_resized
import json
import mysql.connector

'''
Function for retrieving an attribute from a RDS database that is used as
foreign key in another DynamoDb database, and then retrieving the item 
from the DynamoDb database.

This could be done using the event lambda_handler receives, i did it this
instead in order to show you the keys and parameters used.
'''

def lambda_handler(event, context):
    event_for_rds = create_event_for_rds()
    id = retrieve_foreign_key_from_rds_for_dynamo(event_for_rds)
    event_for_dynamo = create_event_for_dynamo()
    item = retrieve_item_from_dynamo_table(event_for_dynamo)
    return item

def retrieve_item_from_dynamo_table(event):
    region_name = event["region_name"]
    dynamodb = boto3.resource('dynamodb', region_name=region_name)
    table_name = event["table_name"]
    table = dynamodb.Table(table_name)
    item_id = event["id"]
    item = table.get_item(
        Key={
            'Id': item_id,
        }
    )
    return item

def create_event_for_dynamo():
    event = dict()
    event["table_name"] = 'mvd_labs'
    event["id"] = '1'
    event["region_name"] = 'sa-east-1'
    return event

def retrieve_foreign_key_from_rds_for_dynamo(event):
    host = event["host"]
    database = event["database"]
    user = event["user"]
    connection = mysql.connector.connect(host=host, database=database, user=user)
    if connection.is_connected():
        print("Type a name")
        name = input() 
        print("Type a surname")
        surname = input()
        cursor = connection.cursor()
        query = create_query(name, surname, database) 
        cursor.execute(query)
        row = cursor.fetchone()
    cursor.close()
    connection.close()
    return row

def create_query(name, surname, database):
    return "select Id from " + database + "where name = '" + name + "' and surname ='" + surname + "'"

def create_event_for_rds():
    event = dict()
    event["host"] = 'database-2.ca4xvkqm7ol9.sa-east-1.rds.amazonaws.com'
    event["database"] = 'employees'
    event["user"] = 'root'
