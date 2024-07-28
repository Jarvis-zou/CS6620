#!/bin/bash
docker build -t rest-api-test -f DockerfileTest .
docker run --network host rest-api-test