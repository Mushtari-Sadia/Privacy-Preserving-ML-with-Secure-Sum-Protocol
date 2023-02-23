#when containers are already running (after running docker-script.sh)

#copying files to each container

for i in {1..3}; do
    # docker exec client$i sh -c "rm ppml_client.py"
    # docker cp "$(pwd)/test.txt" client$i:test.txt
    docker cp "$(pwd)/rsa.py" client$i:rsa.py
    docker cp "$(pwd)/phase_1.py" client$i:phase_1.py
    docker cp "$(pwd)/phase_2.py" client$i:phase_2.py
    docker cp "$(pwd)/phase_3.py" client$i:phase_3.py
    docker cp "$(pwd)/train_parkinsons.csv" client$i:train_parkinsons.csv
    docker cp "$(pwd)/test_parkinsons.csv" client$i:test_parkinsons.csv
    docker cp "$(pwd)/train_susy.csv" client$i:train_susy.csv
    docker cp "$(pwd)/test_susy.csv" client$i:test_susy.csv
    # docker cp "$(pwd)/ppml_client.py" client$i:ppml_client.py
done

# docker exec server sh -c "rm ppml_server.py"
docker cp "$(pwd)/rsa.py" server:rsa.py
docker cp "$(pwd)/phase_1.py" server:phase_1.py
docker cp "$(pwd)/phase_2.py" server:phase_2.py
docker cp "$(pwd)/phase_3.py" server:phase_3.py
docker cp "$(pwd)/phase_4.py" server:phase_4.py
# docker cp "$(pwd)/ppml_server.py" server:ppml_server.py
# docker cp "$(pwd)/test_python.txt" server:test_python.txt
