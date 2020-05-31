#!/bin/bash

sudo docker-compose up -d --build
cd ./tests
pytest
while [ $? -ne 0 ]; do
    pytest
done
cd ..