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

# Load the data
file_path = 'C:/Users/abder/Desktop/2patients/Server_Client/accelerometer_data/accelerometer1.csv'
vitals_file_path = 'C:/Users/abder/Desktop/2patients/Server_Client/vitals_data/vitals1.csv'

from keras.models import load_model
best_model = load_model("best_model.22-0.17.keras")
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

# Normal ranges for vital signs
heart_rate_range = (60.0, 10.0)  # beats per minute
systolic_pressure_range = (90.0, 120.0)  # mmHg
diastolic_pressure_range = (60.0, 80.0)   # mmHg
respiratory_rate_range = (12.0, 20.0)  # breaths per minute
body_temperature_range = (35.9,37.2)  # Celsius
oxygen_saturation_range = (95.0, 100.0)  # percentage

while True:
    try:
        current=datetime.now()

        data = pd.read_csv(file_path)
        data = data.tail(680)
        scaler = StandardScaler()
        data_scaled = scaler.fit_transform(data)
        data_reshaped = data_scaled.reshape(-1, 17, 40, 3)
        
        predictions = best_model.predict(data_reshaped, verbose=None)
        print(predictions)

        predicted_class = (predictions >= 0.4).astype(int)

        ''' vitals = pd.read_csv(vitals_file_path)
        lastrow=vitals.tail(1)

        heart=float(lastrow.heart_rate.iloc[0])
        if not heart_rate_range[0]<=heart<= heart_rate_range[1]:
            send_data_to_server(f' Patient 00001: An abnormal heart rate reading of {heart} has been detected (outside the normal range of {heart_rate_range}). Please check the patient health status.')
            print(f' Patient 00001: An abnormal heart rate  {heart}  reading has been detected (outside the normal range of {heart_rate_range}). Please check the patient health status.')

        systolic_pressure=float(lastrow.systolic_pressure.iloc[0])

        if not systolic_pressure_range[0] <=systolic_pressure<=  systolic_pressure_range[1]:
            send_data_to_server(f' Patient 00001: An abnormal systolic pressure reading  of   {systolic_pressure} has been detected (outside the normal range of {systolic_pressure_range}). Please check the patient health status.')
            print(f' Patient 00001: An abnormal systolic pressure reading  of {systolic_pressure}  has been detected (outside the normal range of {systolic_pressure_range}). Please check the patient health status.')


        diastolic_pressure=float(lastrow.diastolic_pressure.iloc[0])


        if not diastolic_pressure_range[0]<=diastolic_pressure<=  diastolic_pressure_range[1]:
            send_data_to_server(f' Patient 00001: An abnormal diastolic pressure reading  of {diastolic_pressure} has been detected (outside the normal range of {diastolic_pressure_range}). Please check the patient health status.')
            print(f' Patient 00001: An abnormal diastolic pressure reading  of {diastolic_pressure} has been detected (outside the normal range of {diastolic_pressure_range}). Please check the patient health status.')


        respiratory_rate=float(lastrow.respiratory_rate.iloc[0])

        if not respiratory_rate_range[0]<=respiratory_rate<=  respiratory_rate_range[1]:
            send_data_to_server(f' Patient 00001: An abnormal respiratory rate reading of {respiratory_rate} has been detected (outside the normal range of {respiratory_rate_range}). Please check the patient health status.')
            print(f' Patient 00001: An abnormal respiratory rate reading of {respiratory_rate}  has been detected (outside the normal range of {respiratory_rate_range}). Please check the patient health status.')


        body_temperature=float(lastrow.body_temperature.iloc[0])

        if not (body_temperature_range[0]<=body_temperature<= body_temperature_range[1]):
            send_data_to_server(f' Patient 00001: An abnormal body temperature reading of {body_temperature}  has been detected (outside the normal range of{body_temperature_range}). Please check the patient health status.')
            print(f' Patient 00001: An abnormal body temperature reading of {body_temperature} has been detected (outside the normal range of{body_temperature_range}). Please check the patient health status.')


        oxygen_saturation=float(lastrow.oxygen_saturation.iloc[0])

        if not oxygen_saturation_range[0]<=oxygen_saturation<= oxygen_saturation_range[1]:
            send_data_to_server(f' Patient 00001: An abnormal oxygen saturation of{oxygen_saturation} has been detected (outside the normal range of{oxygen_saturation_range}). Please check the patient health status.')
            print(f' Patient 00001: An abnormal oxygen saturation reading of {oxygen_saturation} has been detected (outside the normal range of{oxygen_saturation_range}). Please check the patient health status.')'''
        # Interpret the results


        if predicted_class == 0:
            print("Normal Activity")
            status = 0
        else:
            print("Fall Detected")
            if status == 0:
                try:
                    #send_data_to_server("Patient 00001: A fall has been detected, and the patient may require assistance.")
                    status = 1
                    print('Fall sent to web')
                    #time.sleep(80)
                except:
                    print(' ')

        if keyboard.is_pressed('q'):
            print("Key pressed. Exiting loop.")
            break 
        #print(overall_result)
        #print((datetime.now()-current).total_seconds())
    except:
        if keyboard.is_pressed('q'):
            print("Key pressed. Exiting loop.")
            break 
        pass