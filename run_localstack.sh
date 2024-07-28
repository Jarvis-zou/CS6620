#!/bin/sh
# Check LocalStack status
echo "Checking LocalStack status..."
until curl -s http://localhost:4566/health | grep '"s3": "running"'; do
  echo "Waiting for LocalStack S3 service to be running..."
  sleep 5
done

python ./REST/rest.py

sleep 5

echo "Checking REST API status..."
until curl -s http://localhost:5000/health; do
  echo "Waiting for REST API to be running..."
  sleep 5
done

echo "REST API is running."

tail -f /dev/null