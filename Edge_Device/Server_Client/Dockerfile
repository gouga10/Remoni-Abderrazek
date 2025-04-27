# Use the official Python image as a base image
FROM python:3.12.2

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any dependencies
RUN pip install --no-cache-dir websockets==12.0 asyncio==3.4.3 netifaces==0.11.0  # Add any additional dependencies your script needs

# Command to run your Python script
CMD ["python", "server.py"]
