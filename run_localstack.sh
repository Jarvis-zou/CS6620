#!/bin/sh
localstack start &
python ./REST/rest.py
