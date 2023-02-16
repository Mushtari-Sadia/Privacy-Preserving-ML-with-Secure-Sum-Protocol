

for i in {1..10}; do
    #each client generating their own private and public key
    docker exec -d client$i python phase_1.py $i

    #each client sending their own public key to server
    docker exec -d client$i sh -c "cat public${i}.pkl | nc -w 1 server 8080"
    docker exec -d server sh -c "nc -l 8080 > public${i}.pkl"
done

#server generating own public and private key
docker exec -d server python phase_1.py 0

#server sending all public keys to all clients
for i in {1..10}; do
    for j in {0..10}; do
        docker exec -d server sh -c "cat public${j}.pkl | nc -w 1 client${i} 8080"
        docker exec -d client$i sh -c "nc -l 8080 > public${j}.pkl"
    done
done

#now everyone has all public keys and their own private keys

# for i in {1..10}; do
#     docker exec -d client$i sh -c "rm rsa.py"
#     docker exec -d server sh -c "rm rsa.py"
# done

# for i in {1..10}; do
#     docker exec -d client$i sh -c "rm phase_1.py"
#     docker exec -d server sh -c "rm phase_1.py"
# done

