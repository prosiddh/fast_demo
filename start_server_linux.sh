#!/bin/bash

# Make this script executable
chmod +x start_server_linux.sh

# Install requirements
echo "Installing requirements..."
pip install -r requirements.txt

# Start the server
echo "Starting the server..."
uvicorn app_demo.main:app --port 8005
