import subprocess

# Define the paths to your Python scripts
script1_path = "./Server_Client/server.py"
script2_path = "./Server_Client/Cloud_RealTime.py"

# Launch each script in a separate terminal
subprocess.Popen(["start", "cmd", "/k", "python", script1_path], shell=True)
subprocess.Popen(["start", "cmd", "/k", "python", script2_path], shell=True)