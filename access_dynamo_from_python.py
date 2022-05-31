import boto3
from boto3.dynamodb.conditions import Key
from curses import is_term_resized
import json
import mysql.connector

'''
Function for retrieving an attribute from a RDS database that is used as
foreign key in another DynamoDb database, and then retrieving the item 
from the DynamoDb database.

Usage:
Event = {
    "table_name" : "mvd_labs"
    "id" : "1"
    "region_name" : "sa-east-1"
    "host" : "database-2.ca4xvkqm7ol9.sa-east-1.rds.amazonaws.com"
    "database" : "employees"
    "user" : "root"
}
'''

def lambda_handler(event, context):
    try:
        id = retrieve_foreign_key_from_rds_for_dynamo(event["host"], event["database"], event["user"])
        item = retrieve_item_from_dynamo_table(event["region_name"], event["table_name"], event["id"])
        return item
    except:
        raise Exception("Error, something wrong occurred...")

'''
Function for retrieving an item from a DynamoDb database, receiving a region name, table name, and an item id.
The function returns the item. 
'''

def retrieve_item_from_dynamo_table(region_name, table_name, item_id):
    try:
        dynamodb = boto3.resource('dynamodb', region_name=region_name)
        table = dynamodb.Table(table_name)
        item = table.get_item(
            Key={
                'Id': item_id,
            }
        )
        return item
    except:
        raise Exception("Couldn't retrieve RDS database item")

'''
Function for retrieving an item Id from a RDS database. It receives a host, a database name, and a user 
in order to connect to the database. A query is made receiving a Name and Surname as an input. 
The function returns the id. 
'''

def retrieve_foreign_key_from_rds_for_dynamo(host, database, user):
    try:
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
        else: 
            raise Exception("Connection to DynamoDb failed")
        cursor.close()
        connection.close()
        return row
    except:
        raise Exception("Couldn't retrieve DynamoDb database item")


'''
Function for creating the query retrieving the items with a certain Name and Surname. It also need the
database name. It returns the query in a string.
'''

def create_query(name, surname, database):
    return "select Id from " + database + "where name = '" + name + "' and surname ='" + surname + "'"
