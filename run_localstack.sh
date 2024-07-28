#!/bin/sh

# Check LocalStack status
echo "Checking LocalStack status..."
until curl -s http://localstack:4566/health | grep '"s3": "running"'; do
  echo "Waiting for LocalStack S3 service to be running..."
  sleep 5
done

echo "LocalStack is ready. Starting REST API..."

# Start the REST API
python /app/REST/rest.py
