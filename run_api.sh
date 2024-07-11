#!/bin/bash
docker build -t rest-api -f DockerfileAPI .
docker run -p 5000:5000 rest-api
