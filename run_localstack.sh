#!/bin/sh
localstack start &
echo "Start Localstack..."
sleep 10
python ./REST/rest.py
echo "Start REST API..."

