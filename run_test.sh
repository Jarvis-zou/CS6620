#!/bin/bash
docker build -t rest-api-test -f DockerfileTest .
docker run rest-api-test