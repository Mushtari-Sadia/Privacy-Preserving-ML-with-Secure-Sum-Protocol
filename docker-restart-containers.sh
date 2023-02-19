for i in {1..10}; do
    docker start client$i
done

docker start server

docker ps