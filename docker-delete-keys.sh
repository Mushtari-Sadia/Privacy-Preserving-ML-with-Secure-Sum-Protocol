for i in {1..10}; do
    for j in {0..10}; do
        docker exec -d client$i sh -c "rm public${j}.pkl"
    done
    docker exec -d client$i sh -c "rm private${i}.pkl"
    docker exec -d server sh -c "rm encrypted${i}.pkl"
done

for i in {0..10}; do
    docker exec -d server sh -c "rm public${i}.pkl"
done
docker exec -d server sh -c "rm private0.pkl"

