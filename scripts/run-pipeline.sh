#!/bin/bash

sudo docker-compose up -d
cd ./tests
pytest
while [ $? -ne 0 ]; do
  sleep 30
  pytest
done
cd ..