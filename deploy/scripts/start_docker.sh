#!/bin/bash

# Login to AWS ECR
aws ecr get-login-password --region ap-south-1 | docker login --username AWS --password-stdin 869894982980.dkr.ecr.ap-south-1.amazonaws.com

# Pull the latest image
docker pull 869894982980.dkr.ecr.ap-south-1.amazonaws.com/akshatsharma2407/autonexus:latest

if [ "$(docker ps -q -f name=my-app)" ]; then
    # Stop the running container
    docker stop my-app
fi

# Check if the container 'campusx-app' exists (stopped or running)
if [ "$(docker ps -aq -f name=my-app)" ]; then
    # Remove the container if it exists
    docker rm my-app
fi

# Run a new container
docker run -d -p 80:8000 -e DAGSHUB_PAT=c809196fbed9deeef3e3cbda2ece56af99d4dbeb --name my-app 869894982980.dkr.ecr.ap-south-1.amazonaws.com/akshatsharma2407/autonexus:latest