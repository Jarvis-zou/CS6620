#!/bin/bash
docker build -t rest-api-test -f Dockerfile.test .
docker run rest-api-test