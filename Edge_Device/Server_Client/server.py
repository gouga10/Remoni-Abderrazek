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
from sklearn.preprocessing import StandardScaler
import requests
from dotenv import load_dotenv
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
                #send_data_to_server(f' Patient {patient_id}: An abnormal heart rate reading of {heart} has been detected (outside the normal range of {heart_rate_range}). Please check the patient health status.')
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

# patient  2


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



# patient  1

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




    #Read Accelerometer Data for 2 patients
    df2= pd.read_csv("./accelerometer_data/accelerometer2.csv")
    df1= pd.read_csv("./accelerometer_data/accelerometer1.csv")
    status1=0
    status2=0

    counter=datetime.now()
    while True:
        try:
                # Convert Data from Watch back to JSON string
            json_string = await websocket.recv()
            json_data = json.loads(json_string)
            
            #Generate random vital signs

            
            time_stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            systolic_pressure  = random.randint(91, 100)  # mmHg
            diastolic_pressure  = random.randint(61, 79)   # mmHg
            respiratory_rate  = random.randint(13, 19)  # breaths per minute
            body_temperature  = random.randint(36, 37)  # Celsius
            oxygen_saturation  = random.randint(96, 99)  # percentage
            keys=list(json_data.keys())


    #Check which watch is sending Data

            if 'Accceleration2' in keys:


                # Patient 2
                if 'HeartRate2' in keys:

                    #Vital signs
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


                    #Accelerometer Data and fall model
                Acceleration=json_data['Accceleration2']
                accelerometer={'AccelerationX':Acceleration['ax'], 'AccelerationY':Acceleration['ay'], 'AccelerationZ':Acceleration['az']}
                print('acceleartion2 data: ',accelerometer)

                #Fall detection model inference 
                if len(df2)>=681:
                    df2 = df2[1:]  # keeping accelerometer data file short 681 rowa
                added_row = pd.DataFrame(accelerometer, index=[0])
                df2 = pd.concat([df2, added_row],ignore_index=True)
                data = df2.tail(680)
                scaler = StandardScaler()
                data_scaled = scaler.fit_transform(data)
                data_reshaped = data_scaled.reshape(-1, 17, 40, 3)
                
                predictions = best_model.predict(data_reshaped, verbose=None)
                print(predictions)

                predicted_class = (predictions >= 0.4).astype(int)
                df.to_csv("./accelerometer_data/accelerometer2.csv", index=False)
                predicted_class=0
                if predicted_class == 0:
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

                if keyboard.is_pressed('P'):
                    send_data_to_server("Patient 00002: A fall has been detected, and the patient may require assistance.")

                    pass 
                if keyboard.is_pressed('*'):
                    print("Key pressed. Exiting loop.")
                    df2.to_csv("./accelerometer_data/accelerometer2.csv", index=False)
                    break



                #Patient 1
            else:
                if 'Acceleration1' in keys:
                    if 'HeartRate1' in keys:
                        #Vital signs
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



            #Fall detection model inference

                Acceleration=json_data['Acceleration1']
                accelerometer={'AccelerationX':Acceleration['ax'],'AccelerationY':Acceleration['ay'],'AccelerationZ':Acceleration['az']}
                print('acceleartion1 data: ',accelerometer)

                if len(df1)>=682:
                    df1 = df1[1:]
                added_row = pd.DataFrame(accelerometer, index=[0])
                df1 = pd.concat([df1, added_row],ignore_index=True)
                data = df1.tail(680)
                scaler = StandardScaler()
                data_scaled = scaler.fit_transform(data)
                data_reshaped = data_scaled.reshape(-1, 17, 40, 3)
                predictions = best_model.predict(data_reshaped, verbose=None)
                print(predictions)

                predicted_class = (predictions >= 0.4).astype(int)
                

                predicted_class=0
                if predicted_class == 0:
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

                #Exiting loop from patient 1
                if keyboard.is_pressed('*'):
                    print("Key pressed. Exiting loop.")
                    df1.to_csv("./accelerometer_data/accelerometer1.csv", index=False)
                    break  
            
                #exiting loop outside patient 1 and 2 if the first try worked well
            if keyboard.is_pressed('*'):
                    print("Key pressed. Exiting loop.")
                    df1= pd.read_csv("./accelerometer_data/accelerometer1.csv")
                    df2= pd.read_csv("./accelerometer_data/accelerometer2.csv")
                    break
            if keyboard.is_pressed('/'):
                    send_data_to_server("Patient 00001: A fall has been detected, and the patient may require assistance.")
                    
            

            #If connection problem (in Try)
        except:
            df1.to_csv("./accelerometer_data/accelerometer1.csv", index=False)
            df2= pd.read_csv("./accelerometer_data/accelerometer2.csv")
            print('Connection problem, saving data')
            pass    
                #exiting loop
            if keyboard.is_pressed('*'):
                    print("Key pressed. Exiting loop.")
                    break  
            



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
