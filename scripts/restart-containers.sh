for i in {1..3}; do
    docker start client$i
done

docker start server

docker ps