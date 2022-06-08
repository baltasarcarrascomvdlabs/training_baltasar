import boto3

'''
Function for calculating the number of API calls to the mean temperature API, thisis made by counting the amount of logs generated by the API
'''

def lambda_handler(event, context):
    client = boto3.client('logs')
    logs = client.describe_log_streams(logGroupName='/aws/lambda/temperature-api', logStreamNamePrefix='mduloezzn7')
    length = len(logs['logStreams'])
    response = { "API calls ": length}
    return response
