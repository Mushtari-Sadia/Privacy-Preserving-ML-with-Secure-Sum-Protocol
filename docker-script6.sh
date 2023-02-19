# server sending all encrypted files to client 10
for i in {1..10}; do
        docker exec -d server sh -c "cat encrypted${i}.pkl | nc -w 1 client10 8080"
        docker exec -d client10 sh -c "nc -l 8080 > encrypted${i}.pkl"
done

for i in {10..2}; do
    # client stripping off one layer of encryption
    docker exec -d client$i python phase_3.py $i
    # send all files to next client
    for j in {1..10}; do
        docker exec -d client$i sh -c "cat encrypted${j}.pkl | nc -w 1 client10 8080"
        docker exec -d client$((i-1)) sh -c "nc -l 8080 > encrypted${j}.pkl"
    done
done

# client 1 stripping off one layer of encryption
docker exec -d client1 python phase_3.py 1
# send all files to server
for j in {1..10}; do
    docker exec -d client1 sh -c "cat encrypted${j}.pkl | nc -w 1 server 8080"
    docker exec -d server sh -c "nc -l 8080 > encrypted${j}.pkl"
done