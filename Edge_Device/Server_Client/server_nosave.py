import socket
import asyncio
import websockets
import csv
import os
import random
import json
from datetime import datetime
import netifaces
import time
import pandas as pd


import pandas as pd
from sklearn.preprocessing import StandardScaler
import requests
import time
import os
from dotenv import load_dotenv
from datetime import datetime
import json
import keyboard
# Load environment variables from .env
load_dotenv()

# Access your API key
url = os.getenv("url")



from keras.models import load_model
best_model = load_model("./model/best_model.22-0.17.keras")
# Thresholds based on the distribution
#low_confidence_threshold = 0.4
#high_confidence_threshold = 0.7
confidence_threshold = 0.5

def send_data_to_server(anomalie):
    # Replace 'your-ec2-public-ip' with your EC2 instance's public IP address
    data={'anomaly':anomalie}
    # Send the data as a POST request
    

    json_data = json.dumps(data)
    
    # Send the data as a POST request with Content-Type header set to application/json
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=json_data, headers=headers)
    print(response.status_code)

status = 0







def check_anomalies(vitals,patient_id):
        heart_rate_range = (60.0, 120.0)  # beats per minute
        systolic_pressure_range = (90.0, 120.0)  # mmHg
        diastolic_pressure_range = (60.0, 80.0)   # mmHg
        respiratory_rate_range = (12.0, 20.0)  # breaths per minute
        body_temperature_range = (35.9,37.2)  # Celsius
        oxygen_saturation_range = (95.0, 100.0)  # percentage
        lastrow=vitals.tail(1)

        heart=float(lastrow.heart_rate.iloc[0])
        try:
            if not heart_rate_range[0]<=heart<= heart_rate_range[1]:
                send_data_to_server(f' Patient {patient_id}: An abnormal heart rate reading of {heart} has been detected (outside the normal range of {heart_rate_range}). Please check the patient health status.')
                print(f' Patient {patient_id}: An abnormal heart rate  {heart}  reading has been detected (outside the normal range of {heart_rate_range}). Please check the patient health status.')

            systolic_pressure=float(lastrow.systolic_pressure.iloc[0])

            if not systolic_pressure_range[0] <=systolic_pressure<=  systolic_pressure_range[1]:
                send_data_to_server(f' Patient {patient_id}: An abnormal systolic pressure reading  of   {systolic_pressure} has been detected (outside the normal range of {systolic_pressure_range}). Please check the patient health status.')
                print(f' Patient {patient_id}: An abnormal systolic pressure reading  of {systolic_pressure}  has been detected (outside the normal range of {systolic_pressure_range}). Please check the patient health status.')


            diastolic_pressure=float(lastrow.diastolic_pressure.iloc[0])


            if not diastolic_pressure_range[0]<=diastolic_pressure<=  diastolic_pressure_range[1]:
                send_data_to_server(f' Patient {patient_id}: An abnormal diastolic pressure reading  of {diastolic_pressure} has been detected (outside the normal range of {diastolic_pressure_range}). Please check the patient health status.')
                print(f' Patient {patient_id}: An abnormal diastolic pressure reading  of {diastolic_pressure} has been detected (outside the normal range of {diastolic_pressure_range}). Please check the patient health status.')


            respiratory_rate=float(lastrow.respiratory_rate.iloc[0])

            if not respiratory_rate_range[0]<=respiratory_rate<=  respiratory_rate_range[1]:
                send_data_to_server(f' Patient {patient_id}: An abnormal respiratory rate reading of {respiratory_rate} has been detected (outside the normal range of {respiratory_rate_range}). Please check the patient health status.')
                print(f' Patient {patient_id}: An abnormal respiratory rate reading of {respiratory_rate}  has been detected (outside the normal range of {respiratory_rate_range}). Please check the patient health status.')
                time.sleep(5)

            body_temperature=float(lastrow.body_temperature.iloc[0])

            if not (body_temperature_range[0]<=body_temperature<= body_temperature_range[1]):
                send_data_to_server(f' Patient {patient_id}: An abnormal body temperature reading of {body_temperature}  has been detected (outside the normal range of{body_temperature_range}). Please check the patient health status.')
                print(f' Patient {patient_id}: An abnormal body temperature reading of {body_temperature} has been detected (outside the normal range of{body_temperature_range}). Please check the patient health status.')


            oxygen_saturation=float(lastrow.oxygen_saturation.iloc[0])

            if not oxygen_saturation_range[0]<=oxygen_saturation<= oxygen_saturation_range[1]:
                send_data_to_server(f' Patient {patient_id}: An abnormal oxygen saturation of{oxygen_saturation} has been detected (outside the normal range of{oxygen_saturation_range}). Please check the patient health status.')
                print(f' Patient {patient_id}: An abnormal oxygen saturation reading of {oxygen_saturation} has been detected (outside the normal range of{oxygen_saturation_range}). Please check the patient health status.')
        except:
            pass










# patient  1 
async def handle(websocket, path):
    if not os.path.exists('./vitals_data/vitals00002.csv'):
        with open('./vitals_data/vitals.csv', 'w', newline='') as csvfile:
            fieldnames = ['time_stamp','heart_rate', 'systolic_pressure', 'diastolic_pressure', 'respiratory_rate', 'body_temperature', 'oxygen_saturation']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
    if not os.path.exists('./accelerometer_data/accelerometer2.csv'):
        with open('./accelerometer_data/accelerometer2.csv', 'w', newline='') as csvfile:
            fieldnames = ['AccelerationX', 'AccelerationY', 'AccelerationZ']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()


# patient  2


    if not os.path.exists('./vitals_data/vitals00001.csv'):
        with open('./vitals_data/vitals00001.csv', 'w', newline='') as csvfile:
            fieldnames = ['time_stamp','heart_rate', 'systolic_pressure', 'diastolic_pressure', 'respiratory_rate', 'body_temperature', 'oxygen_saturation']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
    if not os.path.exists('./accelerometer_data/accelerometer1.csv'):
        with open('./accelerometer_data/accelerometer1.csv', 'w', newline='') as csvfile:
            fieldnames = ['AccelerationX', 'AccelerationY', 'AccelerationZ']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()



    df_acc2= pd.read_csv("./accelerometer_data/accelerometer2.csv")
    df_acc1= pd.read_csv("./accelerometer_data/accelerometer1.csv")
    status1=0
    status2=0

    counter=datetime.now()
    while True:
        json_string = await websocket.recv()
        json_data = json.loads(json_string)
        
        

        # Convert back to JSON string
        time_stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        systolic_pressure  = random.randint(91, 100)  # mmHg
        diastolic_pressure  = random.randint(61, 79)   # mmHg
        respiratory_rate  = random.randint(13, 19)  # breaths per minute
        body_temperature  = random.randint(36, 37)  # Celsius
        oxygen_saturation  = random.randint(96, 99)  # percentage
        keys=list(json_data.keys())
        if 'HeartRate2' in keys:
            heart_rate=json_data['HeartRate2']
            if( heart_rate >0) and (heart_rate <200 ): 
                counter2=datetime.now()

                

                vitals={'time_stamp':time_stamp,'heart_rate':heart_rate,'systolic_pressure':systolic_pressure ,'diastolic_pressure':diastolic_pressure ,'respiratory_rate':respiratory_rate ,'body_temperature':body_temperature ,'oxygen_saturation' :oxygen_saturation }
                
                df= pd.read_csv("./vitals_data/vitals00002.csv")
                if len(df)>=41:
                    df = df[1:]
                added_row = pd.DataFrame(vitals, index=[0])
                df = pd.concat([df, added_row],ignore_index=True)
                df.to_csv("./vitals_data/vitals00002.csv", index=False)
                print('new vital file created')


            if heart_rate>150:
                print("patient 0 Heart rate is too high, please contact a doctor")  

            Acceleration=json_data['Acceleration']
            accelerometer={'AccelerationX':Acceleration['ax'], 'AccelerationY':Acceleration['ay'], 'AccelerationZ':Acceleration['az']}


            
            if len(df_acc2)>=681:
                df_acc2 = df_acc2[1:]
            
            added_row2 = pd.DataFrame(accelerometer, index=[0])
            df_acc2 = pd.concat([df_acc2, added_row2],ignore_index=True)
            data2 = df_acc2.tail(680)
            scaler = StandardScaler()
            data_scaled2 = scaler.fit_transform(data2)
            data_reshaped2 = data_scaled2.reshape(-1, 17, 40, 3)
            
            predictions2 = best_model.predict(data_reshaped2, verbose=None)
            print(predictions2)

            predicted_class2 = (predictions2 >= 0.4).astype(int)
            

            if predicted_class2 == 0:
                print("Normal Activity")
                status2 = 0
            else:
                print("Fall Detected")
                if status2 == 0:
                    try:
                        send_data_to_server("Patient 00002: A fall has been detected, and the patient may require assistance.")
                        status2 = 1
                        print('Fall sent to web')
                        
                    except:
                        print(' ')

  

        else:

            heart_rate=json_data['HeartRate1']
            if( heart_rate >0) and (heart_rate <200 ): 
                

                vitals={'time_stamp':time_stamp,'heart_rate':heart_rate,'systolic_pressure':systolic_pressure ,'diastolic_pressure':diastolic_pressure ,'respiratory_rate':respiratory_rate ,'body_temperature':body_temperature ,'oxygen_saturation' :oxygen_saturation }
                df= pd.read_csv("./vitals_data/vitals00001.csv")
                if len(df)>=41:
                    df = df[1:]
                print('vitals data: ',vitals)
                added_row = pd.DataFrame(vitals, index=[0])
                check_anomalies(added_row,1)
                df = pd.concat([df, added_row],ignore_index=True)
                df.to_csv("./vitals_data/vitals00001.csv", index=False)
                print('new vital file created')
                

            


            if heart_rate>150:
                print("patient 1 Heart rate is too high, please contact a doctor")  

            Acceleration=json_data['Acceleration1']
            accelerometer={'AccelerationX':Acceleration['ax'],'AccelerationY':Acceleration['ay'],'AccelerationZ':Acceleration['az']}
            print('acceleartion1 data: ',accelerometer)
            #Fall detection model inference

            
            if len(df_acc1)>=682:
                df_acc1 = df_acc1[1:]
            
            added_row1 = pd.DataFrame(accelerometer, index=[0])
            df_acc1 = pd.concat([df_acc1, added_row1],ignore_index=True)
            data1 = df_acc1.tail(680)
            scaler = StandardScaler()
            data_scaled = scaler.fit_transform(data1)
            data_reshaped1 = data_scaled.reshape(-1, 17, 40, 3)
            predictions1 = best_model.predict(data_reshaped1, verbose=None)
            print(predictions1)

            predicted_class1 = (predictions1 >= 0.4).astype(int)
            print('fall detection model and new acceleration file done')
            if predicted_class1 == 0:
                print("Normal Activity")
                status1 = 0
            else:
                print("Fall Detected")
                if status1 == 0:
                    try:
                        send_data_to_server("Patient 00001: A fall has been detected, and the patient may require assistance.")
                        status1 = 1
                        print('Fall sent to web')
                        
                    except:
                        print(' ')
 
              

def get_ip_address():
    interfaces = netifaces.interfaces()
    for interface in interfaces:
        addresses = netifaces.ifaddresses(interface)
        if netifaces.AF_INET in addresses:
            for addr_info in addresses[netifaces.AF_INET]:
                ip_address = addr_info['addr']
                if ip_address != '127.0.0.1':
                    return ip_address
# Get the IP address of the computer
host_ip = get_ip_address() #socket.gethostbyname(socket.gethostname())
print("Server running at IP:", host_ip)

start_server = websockets.serve(handle, host_ip, 8080)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
