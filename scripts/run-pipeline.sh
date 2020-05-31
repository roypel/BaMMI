#!/bin/bash

docker-compose up -d
cd ../tests
while [ $? -ne 0 ]; do
    pytest
done
