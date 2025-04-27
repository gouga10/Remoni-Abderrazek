import boto3
import pandas as pd
from datetime import datetime
import pandas as pd
from io import StringIO
import time
# set up client
import os
from dotenv import load_dotenv



# Load environment variables from .env
load_dotenv()

# Access your API key
aws_access_key_id = os.getenv("aws_access_key_id")
aws_secret_access_key = os.getenv("aws_secret_access_key")


# define args
upload_wait=5
first=True

start=datetime.now()
while True:
    current=datetime.now() 

    #if ((current-start).total_seconds()>=upload_wait) or (first == True):          Each 30 minutes, the data is uploaded to the cloud

    if (current.minute==30)or(current.minute==0):                                                          # The data is uploaded to the cloud on the 30th minute of each hour
        #DOWNLOADING
        s3 = boto3.client( 
        service_name='s3',
        region_name='us-east-1',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
        )

        computer=pd.read_csv('Server_Client/vitals.csv')


        try:
            # get data from AWS s3
            obj = s3.get_object(Bucket=bucket_name, Key=key)
            data = obj['Body'].read()

            # transform data into dataframe 

            data_decoded = data.decode('utf-8')
            cloud = pd.read_csv(StringIO(data_decoded))
            
        except:
            cloud=computer[: 2]
        print('cloud dataframe shape :',cloud.shape)
        last_computer=computer[-1 :]

        to_upload = pd.concat([cloud,last_computer],ignore_index=True,axis=0)
        to_upload.to_csv('to_upload.csv',index=False)
        to_upload.drop_duplicates(inplace=True)
        print('uploaded dataframe shape :',to_upload.shape)
        to_upload.to_csv('to_upload.csv',index=False)

        #UPLOADING
        s3 = boto3.resource(
            service_name='s3',
            region_name='us-east-1',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key
        )

        file_path = 'to_upload.csv' # local file path
        bucket_name = 'remoni' # name of the data bucket on AWS S3, currently set as 'remoni'
        key = f'00001/time_series/{current.strftime("%Y_%m_%d")[:-3]}.csv' # this is the path to save data inside the above bucket

        # upload data
        s3.meta.client.upload_file(Filename=file_path, Bucket=bucket_name, Key=key)
        time.sleep(60)