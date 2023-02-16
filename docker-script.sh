#!/bin/bash

#Step 1 : Install Docker: First, you need to install 
# Docker on your machine. 
# You can download and install Docker from the official website.


# This will create a file named data.bin
# in the current directory with 1024 random bytes.
dd if=/dev/urandom of=data.bin bs=1 count=1024

# Create the Docker network
docker network create mynetwork

# Create the server container
docker run -itd --name server --network mynetwork python:3-alpine sh
docker exec -it server apk add --no-cache socat
docker exec -d server socat tcp-l:8080,fork exec:'/bin/cat'

# Create the client containers
for i in {1..10}; do
    docker run -itd --name client$i --network mynetwork -v "$(pwd)/data.bin:/data.bin:ro" python:3-alpine sh
    docker exec -it client$i apk add --no-cache netcat-openbsd
    docker exec -d client$i sh -c "nc -w 1 server 8080 < /data.bin" #just an example of how to send a file to server, we dont actually need the data.bin file
done