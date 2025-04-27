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
    




# patient  1 
async def handle(websocket, path):

    counter=0
    while True:
        json_string = await websocket.recv()
        json_data = json.loads(json_string)
        counter+=1
        keys=list(json_data.keys())
        

        if ('table' in keys) :
                data=pd.DataFrame(json_data['table'])
                scaler = StandardScaler()
                data_scaled = scaler.fit_transform(data)
                data_reshaped = data_scaled.reshape(-1, 17, 40, 3)
                predictions = best_model.predict(data_reshaped, verbose=None)
                

                predicted_class = (predictions >= 0.8).astype(int)
                

                
                if predicted_class == 0:
                    print("Normal Activity")
                    status1 = 0
                else:
                    print("Fall Detected")
                    if status1 == 0:
                        status1 = 1
                        try:                            
                            #send_data_to_server("Patient 00001: A fall has been detected, and the patient may require assistance.")                            
                            print('Fall sent to web')
                            
                        except:
                            print(' ')
        
        if ('heart' in keys) :

            time_stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            systolic_pressure  = random.randint(91, 100)  # mmHg
            diastolic_pressure  = random.randint(61, 79)   # mmHg
            respiratory_rate  = random.randint(13, 19)  # breaths per minute
            body_temperature  = random.randint(36, 37)  # Celsius
            oxygen_saturation  = random.randint(96, 99)  # percentage
            heart_rate=json_data['heart']

            if( heart_rate >40) and (heart_rate <200 ): 

                vitals={'time_stamp':time_stamp,'heart_rate':heart_rate,'systolic_pressure':systolic_pressure ,'diastolic_pressure':diastolic_pressure ,'respiratory_rate':respiratory_rate ,'body_temperature':body_temperature ,'oxygen_saturation' :oxygen_saturation }
                added_row = pd.DataFrame(vitals, index=[0])
                added_row.to_csv("./vitals_data/vitals00001.csv", index=False)
                print('vitals added to csv')
                if heart_rate>140:
                    print("patient  Heart rate is too high, please contact a doctor")
                    #send_data_to_server("Patient 00001: A High heart rate value detected, and the patient may require assistance.")         


            















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
