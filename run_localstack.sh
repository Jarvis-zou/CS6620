#!/bin/sh
# Check LocalStack status
echo "Checking LocalStack status..."
curl http://localhost:4566/health

# Start the REST API
python /app/REST/rest.py
