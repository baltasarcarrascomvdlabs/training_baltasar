from datetime import datetime 
import boto3

'''
Function for retrieving the latest EMR cluster id created for excecuting the Spark job
'''

def get_cluster_id(emr):
    dateTimeObj = datetime.now()
    page_iterator = emr.get_paginator('list_clusters').paginate(
        CreatedAfter=datetime(dateTimeObj.year, dateTimeObj.month, dateTimeObj.day)
    )
    for pages in page_iterator:
        for items in pages['Clusters']:
            if items["Name"] == "spark_job_cluster":
                    return items["Id"]

'''
Function for calculating the step duration for a the EMR cluster specified in the parameters
'''

def get_step_duration(emr, cluster_id):
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

'''
Function for returrning the step duration of the Spark job runned in the EMR cluster
'''
    
def lambda_handler(context, event):
    emr = boto3.client('emr')
    cluster_id = get_cluster_id(emr)
    step_duration = get_step_duration(emr, cluster_id)
    response = {'Latest step duration: ': str(step_duration)}
    return response



