#!/bin/sh
localstack start &
sleep 10
python ./REST/rest.py
