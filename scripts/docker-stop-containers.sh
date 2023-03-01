for i in {1..3}; do
    docker stop client$i
done

docker stop server

docker ps