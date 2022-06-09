import argparse
from pyspark.sql.functions import mean
from pyspark.sql import SparkSession
import utils

def calculate_mean_temperature(data_source, output_uri, secret_key):
    '''
    Function for retrieving daily temperatures, and calculating the mean temperature. The function writes the result in a csv file into an S3 Bucket.

    Parameters:
        data_source (string): Path to the csv with the temperatures data
        output_uri (string): Path to the folder to write a csv with the results
        secret_key (string): Credential containing the secret key access  for AWS

    Returns:
        None
    '''

    with SparkSession.builder.appName("Calculate Mean Temperature").getOrCreate() as spark:
        if data_source is not None:
            spark._jsc.hadoopConfiguration().set("fs.s3a.access.key", "AKIARMQK4AWGF7SZTZVD")
            spark._jsc.hadoopConfiguration().set("fs.s3a.secret.key", secret_key)
            weather_df = spark.read.option("header", "true").csv(data_source).withColumnRenamed("TEMPERATURA MÍNIMA NA HORA ANT. (AUT) (°C)", "MaximumLastHourTemperature")
            date = utils.get_date_path()
            morning = "10:00"
            temperatures_measured_daily = weather_df.select('MaximumLastHourTemperature').filter((weather_df.Hora == morning) & (weather_df.Data == date) & (weather_df.MaximumLastHourTemperature > -100))
            mean_temperature = temperatures_measured_daily.select(mean('MaximumLastHourTemperature'))
            mean_temperature.write.option("header", "true").mode("overwrite").csv(output_uri + date)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--secret_key')
    parser.add_argument('--data_source')
    parser.add_argument('--output_uri')
    args = parser.parse_args()
    calculate_mean_temperature(args.data_source, args.output_uri, args.secret_key)

			