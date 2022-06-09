import boto3

def lambda_handler(event, context):
    '''
    Function for calculating the number of API calls to the mean temperature API, thisis made by counting the amount of logs generated by the API

    Parameters:
        context: Not used 
        event: Not used

    Returns:
        JSON: response
    '''

    client = boto3.client('logs')
    logs = client.describe_log_streams(logGroupName='/aws/lambda/temperature-api', logStreamNamePrefix='mduloezzn7')
    length = len(logs['logStreams'])
    response = { "API calls ": length}
    return response
