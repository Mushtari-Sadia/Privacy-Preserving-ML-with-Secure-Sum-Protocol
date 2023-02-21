#when containers are already running (after running docker-script.sh)

#copying files to each container

for i in {1..3}; do
    docker cp "$(pwd)/test.txt" client$i:test.txt
    docker cp "$(pwd)/rsa.py" client$i:rsa.py
    docker cp "$(pwd)/phase_1.py" client$i:phase_1.py
    docker cp "$(pwd)/phase_2.py" client$i:phase_2.py
    docker cp "$(pwd)/phase_3.py" client$i:phase_3.py
done

docker cp "$(pwd)/rsa.py" server:rsa.py
docker cp "$(pwd)/phase_1.py" server:phase_1.py
docker cp "$(pwd)/phase_2.py" server:phase_2.py
docker cp "$(pwd)/phase_3.py" server:phase_3.py
docker cp "$(pwd)/phase_4.py" server:phase_4.py
