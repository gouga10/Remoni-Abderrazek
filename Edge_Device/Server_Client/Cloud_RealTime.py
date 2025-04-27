import requests
import pandas as pd
import csv 
import cv2
import time
import boto3
from io import StringIO
import keyboard
import os
from dotenv import load_dotenv
from datetime import datetime
import ast
# Load environment variables from .env
load_dotenv()

# Access your API key
aws_access_key_id = os.getenv("aws_access_key_id")
aws_secret_access_key = os.getenv("aws_secret_access_key")
s3 = boto3.client( 
            service_name='s3',
            region_name='us-east-1',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key
            )



url = os.getenv("url")



def data_request(patient_id):
    if patient_id == 2:
        df=pd.read_csv('C:/Users/abder/Desktop/2patients - only 2 files/Server_Client/vitals_data/vitals00002.csv')
    if patient_id == 1:
        df=pd.read_csv('C:/Users/abder/Desktop/2patients - only 2 files/Server_Client/vitals_data/vitals00001.csv')

    real_time_data=df[-1 :]
    real_time_data.to_csv(f'./vitals_data/real_time_data.csv',index=False)
    with open('./vitals_data/real_time_data.csv', 'r') as file:
        files = {'file': file}
        s3 = boto3.resource(
            service_name='s3',
            region_name='us-east-1',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key
        )

        file_path = './vitals_data/real_time_data.csv' # local file path
        bucket_name = 'remoni' # name of the data bucket on AWS S3, currently set as 'remoni'
        key = f'real_time_data.csv' # this is the path to save data inside the above bucket

        # upload data
        s3.meta.client.upload_file(Filename=file_path, Bucket=bucket_name, Key=key)
        print(real_time_data)
    
   # return vital_data   



def image_request(frame):
    #snapping a frame from the camera
    
    
    
    # Save the frame
    frame_path = './photos/instant.jpg'
    cv2.imwrite(frame_path, frame)
    print('Captured image.')

    # Path to the image file you want to send
    image_path = './photos/instant.jpg'
    # Open the image file in binary mode and send it as a POST request
    with open(image_path, 'rb') as image_file:
        
        s3 = boto3.resource(
            service_name='s3',
            region_name='us-east-1',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key
        )

        file_path = image_path # local file path
        bucket_name = 'remoni' # name of the data bucket on AWS S3, currently set as 'remoni'
        key = f'instant.jpg' # this is the path to save data inside the above bucket

        # upload data
        s3.meta.client.upload_file(Filename=file_path, Bucket=bucket_name, Key=key)
        print('Sent image to the cloud.')
        
    
    
    
         
def delete_file_from_s3(bucket_name, file_key):
    # Initialize the S3 client
    
    try:
        # Delete the file from the S3 bucket
        s3.delete_object(Bucket=bucket_name, Key=file_key)
        print(f"File '{file_key}' deleted successfully from bucket '{bucket_name}'")
    except Exception as e:
        print(f"Error deleting file '{file_key}' from bucket '{bucket_name}': {str(e)}")


def update_picture_cloud(frame,patient_id,time_stamp):
    s3 = boto3.resource(
    service_name='s3',
    region_name='us-east-1',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key
)
                                      
    # Save the frame
    frame_path = os.path.join( f'photos/frame.jpg')
    cv2.imwrite(frame_path, frame)
    

    date, time = time_stamp.strftime("%Y-%m-%d %H:%M:%S").split(' ')
    # Further split the date into year, month, and day
    year, month, day = date.split('-')
    # Format the year and month as 'YYYY - MM'
    # Format the day and time as 'DD_HH_MM'
    day_time = f'{day}_{time.replace(":", "_")}'
    day_time = day_time[:-3]



    file_path = frame_path # local file path
    bucket_name = 'remoni' # name of the data bucket on AWS S3, currently set as 'remoni'
    if patient_id == 2:
        key = f'00001/image/{time_stamp.strftime("%Y_%m_%d")[:-3]}/{day_time}.jpg' # this is the path to save data inside the above bucket
    else:
        key = f'00002/image/{time_stamp.strftime("%Y_%m_%d")[:-3]}/{day_time}.jpg'
    s3.meta.client.upload_file(Filename=file_path, Bucket=bucket_name, Key=key)
    print("picture uploaded")

def update_vital_cloud(patient_id,time_stamp):
        s3 = boto3.client( 
        service_name='s3',
        region_name='us-east-1',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
        )
        if patient_id == 2:
            computer=pd.read_csv('./vitals_data/vitals00002.csv')
            file_path = './vitals_data/to_upload.csv' # local file path
            bucket_name = 'remoni' # name of the data bucket on AWS S3, currently set as 'remoni'
            key = f'00001/time_series/{time_stamp.strftime("%Y_%m_%d")[:-3]}.csv' # this is the path to save data inside the above bucket
        if patient_id == 1:
            computer=pd.read_csv('./vitals_data/vitals00001.csv')
            file_path = './vitals_data/to_upload.csv'
            bucket_name = 'remoni'
            key = f'00002/time_series/{time_stamp.strftime("%Y_%m_%d")[:-3]}.csv'
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
        #to_upload.to_csv('./vitals_data/to_upload.csv',index=False)
        to_upload.drop_duplicates(inplace=True)
        print('uploaded dataframe shape :',to_upload.shape)
        to_upload.to_csv('./vitals_data/to_upload.csv',index=False)

        #UPLOADING
        s3 = boto3.resource(
            service_name='s3',
            region_name='us-east-1',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key
        )

        

        # upload data
        s3.meta.client.upload_file(Filename=file_path, Bucket=bucket_name, Key=key)
      
f1=False
f2=False
try:    
    cap2 = cv2.VideoCapture(0)
except: 
    pass
try:
    cap1 = cv2.VideoCapture(1)
except:
    pass
last_update=datetime.now()

while True:
    time_stamp=datetime.now()
    if cap2.isOpened():
        ret2, frame2 = cap2.read()
        f2=True
    if cap1.isOpened():    
        ret1, frame1 = cap1.read()
        f1=True

    if (time_stamp-last_update).total_seconds()>=60:

        if (time_stamp.minute==30)or(time_stamp.minute==0): 

            print('uploading')
            if f2:
                update_picture_cloud(frame2,2,time_stamp)
            if f1:
                update_picture_cloud(frame1,1,time_stamp)
            
            update_vital_cloud(2,time_stamp)
            update_vital_cloud(1,time_stamp)

            print('uploaded')
            last_update=time_stamp
    try:
        
        # define args 
        bucket_name = 'remoni' # name of the data bucket on AWS s3, currently set as 'remoni'
        key = f'signal_file.json' # this is the path to save data inside the above bucket

        obj = s3.get_object(Bucket=bucket_name, Key=key)
        data = obj['Body'].read()
        data_decoded = data.decode('utf-8')
        data_decoded = ast.literal_eval(data_decoded)
        print('found request for :', data_decoded)
        print(type(data_decoded))

        delete_file_from_s3(bucket_name, key)
        patient_id = data_decoded['patient_id']

        

        type_of_data=data_decoded['type_of_data']
        
        if patient_id == '00001':
            if type_of_data=='vital_sign':
                data_request(1)
                print('vital sign sent for patient 00001')
                
            elif type_of_data=='image':   
                image_request(frame1)
                print('image sent for patient 00001')
        if patient_id == '00002':
            if type_of_data=='vital_sign':
                data_request(2)
                print('vital sign sent for patient 00002')
            elif type_of_data=='image':   
                image_request(frame2)
                print('image sent for patient 00002')
        
        if keyboard.is_pressed('*'):
            print("Key pressed. Exiting loop.")
            break

        
    except :
        if keyboard.is_pressed('*'):
            print("Key pressed. Exiting loop.")
            break 
        pass
if cap2.isOpened():
    cap2.release()
if cap1.isOpened():
    cap1.release()
