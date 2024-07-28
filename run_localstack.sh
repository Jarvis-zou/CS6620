#!/bin/sh

# Start LocalStack in detached mode
localstack start -d

# Wait for LocalStack to be ready
echo "Waiting for LocalStack to be ready..."
sleep 10

# Check LocalStack status
echo "Checking LocalStack status..."
curl http://localhost:4566/health

# Start the REST API
python /app/REST/rest.py
