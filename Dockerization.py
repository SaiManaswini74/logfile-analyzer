# Use the official Python image from Docker Hub
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the application's dependencies file and install them
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /app

# Expose the port the application runs on
EXPOSE 8000

# Define environment variables, if necessary
ENV ENV=production

# Run the application
CMD ["python", "wisecow.py"]



nce the Dockerfile is ready, you can build and run the Docker image:

Build the Docker Image:

Bash
docker build -t wisecow-app .


Run the Docker Container:

run the Docker Image:
Bash
docker run -p 8000:8000 wisecow-app