#when containers are already running (after running docker-script.sh)

#copying files to each container

for i in {1..10}; do
    docker cp "$(pwd)/rsa.py" client$i:rsa.py
    docker cp "$(pwd)/phase_1.py" client$i:phase_1.py
done

docker cp "$(pwd)/rsa.py" server:rsa.py
docker cp "$(pwd)/phase_1.py" server:phase_1.py