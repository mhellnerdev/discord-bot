#!/bin/sh

docker rm boto3-discord-bot -f

docker rmi boto3-discord-bot -f

docker rmi $(docker images -f "dangling=true" -q)

docker image build -t boto3-discord-bot .

docker run --name "boto3-discord-bot" -d boto3-discord-bot