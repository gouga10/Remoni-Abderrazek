import socket
import asyncio
import websockets
import csv
import os

async def handle(websocket, path):
    if not os.path.exists('data.csv'):
        with open('data.csv', 'w', newline='') as csvfile:
            fieldnames = ['Data']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

    while True:
        json_data = await websocket.recv()
        print("Received  Data:", json_data)

        # Write the received JSON data to the CSV file
        with open('data.csv', 'a', newline='') as csvfile:
            fieldnames = ['Data']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow({'Data': json_data})

# Get the IP address of the computer
host_ip = socket.gethostbyname(socket.gethostname())
print("Server running at IP:", host_ip)

start_server = websockets.serve(handle, host_ip, 8080)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
