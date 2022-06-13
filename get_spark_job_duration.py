from datetime import datetime 
import boto3

def get_cluster_id(emr):
    '''
    Function for retrieving the latest EMR cluster id created for excecuting the Spark job

    Parameters:
        emr (Boto3.client.EMR): EMR object of the Boto3.Client class

    Returns:
        string: EMR_Id
    '''

    dateTimeObj = datetime.now()
    page_iterator = emr.get_paginator('list_clusters').paginate(
        CreatedAfter=datetime(dateTimeObj.year, dateTimeObj.month, dateTimeObj.day)
    )
    for pages in page_iterator:
        for items in pages['Clusters']:
            if items["Name"] == "spark_job_cluster":
                    EMR_Id =items["Id"]
                    return EMR_Id

def get_step_duration(emr, cluster_id):
    '''
    Function for calculating the step duration for a the EMR cluster specified in the parameters

    Parameters:
        emr (Boto3.client.EMR): EMR object of the Boto3.Client class
        cluster_id (String): Id of the cluster that contains the step wanted

    Returns:
        Datetime.date: step_duration
    '''

    dateTimeObj = datetime.now()
    page_iterator = emr.get_paginator('list_steps').paginate(
        ClusterId=cluster_id
    )
    for pages in page_iterator:
        items =pages['Steps'][0]
        StartDateTime = items['Status']['Timeline']['StartDateTime']
        EndDateTime = items['Status']['Timeline']['EndDateTime']
        step_duration = EndDateTime - StartDateTime
        return step_duration
    
def lambda_handler(context, event):
    '''
    Function for returning the step duration of the Spark job runned in the EMR cluster

    Parameters:
        context: Not used 
        event: Not used

    Returns:
        JSON: response
    '''

    emr = boto3.client('emr')
    cluster_id = get_cluster_id(emr)
    step_duration = get_step_duration(emr, cluster_id)
    response = {'Latest step duration: ': str(step_duration)}
    return response



