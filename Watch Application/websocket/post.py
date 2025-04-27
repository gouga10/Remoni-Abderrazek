import asyncio
import websockets

async def send_data():
    uri = "ws://192.168.136.53:8080"  # WebSocket server address
    async with websockets.connect(uri) as websocket:
        data = input("Enter data to send: ")  # Input data to send
        await websocket.send(data)
        print(f"Data '{data}' sent successfully.")

# Create a new event loop
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

try:
    loop.run_until_complete(send_data())
finally:
    loop.close()
