#!/bin/bash

#Step 1 : Install Docker: First, you need to install 
# Docker on your machine. 
# You can download and install Docker from the official website.


# This will create a file named data.bin
# in the current directory with 1024 random bytes.
dd if=/dev/urandom of=data.bin bs=1 count=1024
# Create the Docker image from dockerfile
docker pull continuumio/anaconda3
docker build -t continuumio/anaconda3 .
# Create the Docker network
docker network create ssumnet

# Create the server container
docker run -itd --name server --network ssumnet continuumio/anaconda3 sh

docker exec server apt-get update
docker exec server apt-get install netcat-openbsd

# Create the client containers
for i in {1..3}; do
    docker run -itd --name client$i --network ssumnet -v "$(pwd)/data.bin:/data.bin:ro" continuumio/anaconda3 sh
    docker exec client$i apt-get update
    docker exec client$i apt-get install netcat-openbsd
    docker exec -d client$i sh -c "nc server 8080 < /data.bin" #just an example of how to send a file to server, we dont actually need the data.bin file
done