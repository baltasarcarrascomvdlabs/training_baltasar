import json
import boto3
import base64

client = boto3.client('emr')
region_name = "us-east-1"

'''
Funciton for retrieving secret key from SecretsManager service
'''

def get_secret():
    secret_name = "secret-key-baltasar"
    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager', region_name=region_name)
    get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    if 'SecretString' in get_secret_value_response:
            secret = get_secret_value_response['SecretString']
    else:
            secret = base64.b64decode(get_secret_value_response['SecretBinary'])
    return json.loads(secret)
    
'''
Function for retrieving stack outputs in order to use them as arguments in the EMR cluster
'''
    
def get_outputs():
    cloudformationf_client = boto3.client('cloudformation')
    stackname = 'ramp-up-baltasar'
    response = cloudformation_client.describe_stacks(StackName=stackname)
    outputs = response["Stacks"][0]["Outputs"]
    for output in outputs:
        keyName = output["OutputKey"]
        if keyName == "ServiceRole":
            ServiceRole = output["OutputValue"]
        if keyName == "JobFlowRole":
            JobFlowRole = output["OutputValue"]
        if keyName == "Ec2SubnetId":
            Ec2SubnetId = output["OutputValue"]
    return (ServiceRole, JobFlowRole, Ec2SubnetId)

'''
Function for running an EMR cluster to excecute a Spark job. The cluster is terminated when the job ends
'''

def lambda_handler(event, context):
    secret = get_secret()
    (ServiceRole, JobFlowRole, Ec2SubnetId) = get_outputs()
    response = client.run_job_flow(
        Name= 'spark_job_cluster',
        LogUri= 's3://emr-test-bucket-baltasar/logs',
        ReleaseLabel= 'emr-6.0.0',
        Instances={
            'MasterInstanceType': 'm5.xlarge',
            'SlaveInstanceType': 'm5.large',
            'InstanceCount': 1,
            'KeepJobFlowAliveWhenNoSteps': False,
            'TerminationProtected': False,
            'Ec2SubnetId': Ec2SubnetId
        },
        Applications = [ {'Name': 'Spark'} ],
        Configurations = [
            { 'Classification': 'spark-hive-site',
              'Properties': {
                  'hive.metastore.client.factory.class': 'com.amazonaws.glue.catalog.metastore.AWSGlueDataCatalogHiveClientFactory'}
            }
        ],
        VisibleToAllUsers=True,
        JobFlowRole = JobFlowRole,
        ServiceRole = ServiceRole,
        Steps=[
            {
                'Name': 'spark_job',
                'ActionOnFailure': 'TERMINATE_CLUSTER',
                'HadoopJarStep': {
                        'Jar': 'command-runner.jar',
                        'Args': [
                            'spark-submit',
                            '--deploy-mode', 'cluster',
                            '--executor-memory', '6G',
                            '--num-executors', '1',
                            '--executor-cores', '2',
                            '--class', 'com.aws.emr.ProfitCalc',
                            's3://emr-test-bucket-baltasar/calculate_mean_temperature.py',
                            '--data_source','s3://emr-test-bucket-baltasar/southeast.csv',
                            '--output_uri','s3://emr-test-bucket-baltasar/mean_temperatures/',
                            '--secret_key', secret["fs.s3a.secret.key"]
                        ]
                }
            }
        ]
    )

