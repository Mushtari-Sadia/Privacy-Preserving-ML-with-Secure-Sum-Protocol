for i in {1..10}; do
    #each client encrypting local file with all public keys
    docker exec client$i python phase_2.py $i
    docker logs -f client$i
    #each client sending their own encrypted file to server
    docker exec -d client$i sh -c "cat encrypted${i}.pkl | nc -w 1 server 8080"
    docker exec -d server sh -c "nc -l 8080 > encrypted${i}.pkl"
done