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