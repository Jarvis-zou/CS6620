#!/bin/bash
docker build -t rest-api -f Dockerfile.api .
docker run -p 5000:5000 rest-api
