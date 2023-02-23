# this script checks if each client has the list of all keys
for i in {1..10}; do
    for j in {0..10}; do
        echo "client$i public$j"
        docker exec client$i sh -c "cat public${j}.pkl"
        echo -e "\n\n"
    done
done
