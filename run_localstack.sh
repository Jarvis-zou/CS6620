#!/bin/sh
echo "Starting LocalStack..."
localstack start &

# Wait for LocalStack to be ready
echo "Waiting for LocalStack to be ready..."
sleep 20

# Check LocalStack status
echo "Checking LocalStack status..."
until curl -s http://localhost:4566/health | grep '"s3": "running"'; do
  echo "Waiting for LocalStack S3 service to be running..."
  sleep 5
done

python ./REST/rest.py
