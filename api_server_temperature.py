import boto3
import csv
import utils

def get_object_path_prefix():
    '''
    Function for getting the path prefix for accesing the mean temperature file stored in the S3 bucket

    Parameters:
        None

    Returns:
        str: path_prefix
    '''

    date = utils.get_date_path()
    path_prefix = 'mean_temperatures/' + date 
    return path_prefix

def get_object_filename(s3_bucket):
    '''
    Function for getting mean temperature file name, which is automatically generated by hadoop in the spark job

    Parameters:
        s3_bucket (Boto3.client.S3): S3 bucket object that contains the mean temperature file

    Returns:
        str: path_prefix
    '''

    path_prefix = get_object_path_prefix()
    s3_objects = s3_bucket.objects.all()
    for my_bucket_object in s3_objects:
        if(my_bucket_object.key.startswith(path_prefix) and my_bucket_object.key.endswith("csv")):
            filename = my_bucket_object.key
    return filename

def read_csv(file):
    '''
    Function for reading a csv file not using its path, but instead the actual file

    Parameters:
        file (Boto3.client.S3.Object): Mean temperature file obtained from S3 bucket

    Returns:
        csv.Object: 
    '''

    data = file['Body'].read().decode('utf-8').splitlines() 
    csv_file = csv.reader(data)
    return csv_file

def lambda_handler(context, event):
    '''
    Function for returning the mean temperature calculated today. It retrieves the data from the csv generated 
    in the spark job and stored in a S3 bucket. The csv file is read and the temperature is obtained.

    Parameters:
        context: Not used 
        event: Not used

    Returns:
        JSON:response
    '''

    s3_resource = boto3.resource(service_name='s3')
    s3_bucket = s3_resource.Bucket('emr-test-bucket-baltasar')
    filename = get_object_filename(s3_bucket)
    mean_temperature_file = s3_bucket.Object(filename).get()
    mean_temperature_csv = read_csv(mean_temperature_file)
    for value in mean_temperature_csv:
        MaximumLastHourTemperature = value
    response = {"Mean temperature today": MaximumLastHourTemperature}
    return response



