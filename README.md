# CSE-472-Project

# 28-jan-23

- installed docker desktop from here : https://www.docker.com/
- after running docker desktop, checked out following articles
     - https://medium.com/techanic/docker-containers-ipc-using-sockets-part-1-2ee90885602c
     - https://medium.com/techanic/docker-containers-ipc-using-sockets-part-2-834e8ea00768
    articles can be found in the resources/docker test directory.
- check out running docker images with the command `docker images`
- if there is no 'my_ipc_server' container running, `docker build -t my_ipc_server .` otherwise go to next step.
- to start the container `docker run -p 9898:9898 my_ipc_server`
- open another terminal and execute `python ipc_client.py`

some handy docker commands :
- docker ps (to see running containers)
- docker stop [container]
- docker restart [container]
- sudo aa-remove-unknown (if docker container refuses to stop)
- 
  To copy files from host machine to a docker container :
- docker cp /path/to/local/file.txt container_name:/path/to/container/file.txt
- 
  To check files inside container
- docker exec -it container_name /bin/bash
    cd /path/to/container
    ls

# 17-feb-23

Implementing Secure-Sum Protocol
================================

Simulated 10 computers (container names : client1...client10) and a mediator (container name : server) using docker containers.

To run a bash script, first set permission : `chmod +x script_name.sh`, then run `./script_name.sh`. Run the following scripts in order.

- docker-script.sh

creates a network of docker containers. Creates all the clients and mediator and connects them in a bridge network named mynetwork. To inspect the network you can run the following command `docker network inspect mynetwork`


- docker-script2.sh

Copies the rsa implementation and a script to generate private and public keys to each machine.


- docker-script3.sh

Installs necessary libraries to run provided python scripts in each machine.

- docker-script4.sh

Generates private and public key for every single machine locally. Then sends all public keys to all machines. So every single machine has all public keys, but only own private key. To check, do the following :

`docker exec -it <container_name> sh`


`ls`


`exit`

Again, container names are : client1...client10 and server.

Next work : Put individual data files into container of each party. Then write a script so that each party shards the data into 4 parts, encrypts the shards in the following order of encryption key -> public0 ... public10. (public0 is server's own public key) Then sends encrypted shards to server. Upon receiving, server shuffles all data segments then sends the entire data to client10. client10 decrypts and sends to client9. client9 decrypts and sends to client8.. and so forth, until client1 sends data back to server, then server decrypts data with own private key.





