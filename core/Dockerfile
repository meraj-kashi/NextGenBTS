# Use an official Python runtime as the base image
FROM python:3.9-slim

RUN apt-get update && apt-get install -y iputils-ping

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file to the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the app code to the container
COPY . .

# Expose the port that the app will run on
EXPOSE 5000

# Run the app when the container starts
CMD ["python", "main.py"]
