

for i in {1..3}; do
    #each client generating their own private and public key
    docker exec -d client$i python phase_1.py $i
    sleep 4
    #each client sending their own public key to server

    docker cp client$i:public${i}.pkl "$(pwd)/public${i}.pkl"
    docker cp "$(pwd)/public${i}.pkl" server:public${i}.pkl
    
done

#server generating own public and private key
docker exec -d server python phase_1.py 0
sleep 4
#server sending all public keys to all clients
for i in {1..3}; do
    for j in {0..3}; do
        
        docker cp server:public${j}.pkl "$(pwd)/public${j}.pkl"
        docker cp "$(pwd)/public${j}.pkl" client$i:public${j}.pkl
        
    done
done

#now everyone has all public keys and their own private keys

# for i in {0..3}; do
#     rm public${i}.pkl
# done


