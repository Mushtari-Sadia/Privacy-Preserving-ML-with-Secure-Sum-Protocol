CONTAINER_NAME=server
if docker inspect --format '{{.State.Status}}' "$CONTAINER_NAME" | grep -q "running"; then
    echo ""
else
    chmod +x restart-containers.sh
    ./restart-containers.sh
fi



docker exec server sh -c "rm params.pkl"
docker exec server sh -c "rm bias.pkl"
docker cp "$(pwd)/linreg_server.py" server:linreg_server.py
for i in {1..3}; do
    docker exec client$i sh -c "rm loss${i}.pkl"
    docker exec client$i sh -c "rm gradient${i}.pkl"
    docker exec client$i sh -c "rm dbias${i}.pkl"
    docker exec client$i sh -c "rm params.pkl"
    docker exec client$i sh -c "rm bias.pkl"
    docker cp "$(pwd)/dataset.py" client$i:dataset.py
    docker cp "$(pwd)/linreg.py" client$i:linreg.py
    docker cp "$(pwd)/linreg_client.py" client$i:linreg_client.py
    docker cp "$(pwd)/linreg_client_inference.py" client$i:linreg_client_inference.py
done

start_time=$(date +%s)

# until convergence is true
# temporarily using 10 epochs
for i in {1}; do

    # run all linreg_client.py in all clients
    echo "Epoch $i"
    for j in {1..3}; do
        docker exec client$j sh -c "python linreg_client.py $j"
        # send losses and gradients to server

        docker exec -d server sh -c "rm loss${j}.pkl"
        docker exec -d server sh -c "nc -l -v -p 1234 -w 1 > loss${j}.pkl"
        docker exec client$j sh -c "cat loss${j}.pkl | nc -v server 1234"
        sleep 1

        while [ true ];do
            filesize=$(docker exec server stat -c%s loss${j}.pkl)
            if [ $filesize -eq 0 ]; then
                echo "Container $j: sending loss${j}.pkl failed, retrying"
                docker exec -d server sh -c "nc -l -v -p 1234 -w 1 > loss${j}.pkl"
                docker exec client$j sh -c "cat loss${j}.pkl | nc -v server 1234"
                sleep 1
            else 
                echo "Container $j: sending loss${j}.pkl succeeded"
                break
            fi
        done

        docker exec -d server sh -c "rm gradient${j}.pkl"
        docker exec -d server sh -c "nc -l -v -p 1234 -w 1 > gradient${j}.pkl"
        docker exec client$j sh -c "cat gradient${j}.pkl | nc -v server 1234"
        sleep 1

        while [ true ];do
            filesize=$(docker exec server stat -c%s gradient${j}.pkl)
            if [ $filesize -eq 0 ]; then
                echo "Container $j: sending gradient${j}.pkl failed, retrying"
                docker exec -d server sh -c "nc -l -v -p 1234 -w 1 > gradient${j}.pkl"
                docker exec client$j sh -c "cat gradient${j}.pkl | nc -v server 1234"
                sleep 1
            else 
                echo "Container $j: sending gradient${j}.pkl succeeded"
                break
            fi
        done

        docker exec -d server sh -c "rm dbias${j}.pkl"
        docker exec -d server sh -c "nc -l -v -p 1234 -w 1 > dbias${j}.pkl"
        docker exec client$j sh -c "cat dbias${j}.pkl | nc -v server 1234"
        sleep 1

        while [ true ];do
            filesize=$(docker exec server stat -c%s dbias${j}.pkl)
            if [ $filesize -eq 0 ]; then
                echo "Container $j: sending dbias${j}.pkl failed, retrying"
                docker exec -d server sh -c "nc -l -v -p 1234 -w 1 > dbias${j}.pkl"
                docker exec client$j sh -c "cat dbias${j}.pkl | nc -v server 1234"
                sleep 1
            else 
                echo "Container $j: sending dbias${j}.pkl succeeded"
                break
            fi
        done
    done

    echo "Server: aggregating losses and gradients"

    # run linreg_server.py in server
    docker exec server sh -c "python linreg_server.py"

    # send params and bias to all clients
    for j in {1..3}; do
        echo "Container $j: sending params.pkl"
        docker exec -d client$j sh -c "rm params.pkl"
        # echo "reaches here 1"
        docker exec -d client$j sh -c "nc -l -p 1234 -w 5 > params.pkl"
        # echo "reaches here 2"
        docker exec server sh -c "cat params.pkl | nc -v -w 5 client$j 1234"
        # echo "reaches here 3"
        # sleep 1

        while [ true ];do
            filesize=$(docker exec client$j stat -c%s params.pkl)
            if [ $filesize -eq 0 ]; then
                echo "Container $j: sending params.pkl failed, retrying"
                docker exec -d client$j sh -c "nc -l -p 1234 -w 5 > params.pkl"
                docker exec server sh -c "cat params.pkl | nc -v -w 5 client$j 1234"
                sleep 1
            else 
                echo "Container $j: sending params.pkl succeeded"
                break
            fi
        done

        echo "Container $j: sending bias.pkl"
        docker exec -d client$j sh -c "rm bias.pkl"
        # echo "reaches here 1"
        docker exec -d client$j sh -c "nc -l -p 1234 -w 5 > bias.pkl"
        # echo "reaches here 2"
        docker exec server sh -c "cat bias.pkl | nc -v -w 5 client$j 1234"
        # echo "reaches here 3"
        # sleep 1

        while [ true ];do
            filesize=$(docker exec client$j stat -c%s bias.pkl)
            if [ $filesize -eq 0 ]; then
                echo "Container $j: sending bias.pkl failed, retrying"
                docker exec -d client$j sh -c "nc -l -p 1234 -w 5 > bias.pkl"
                docker exec server sh -c "cat bias.pkl | nc -v -w 5 client$j 1234"
                sleep 1
            else 
                echo "Container $j: sending bias.pkl succeeded"
                break
            fi
        done

    done
done


for j in {1..3}; do
    docker exec client$j sh -c "python linreg_client_inference.py $j 'dt'"
done;
end_time=$(date +%s)

elapsed_time=$(( end_time - start_time ))

echo "linreg: Latency for distributed trusted: ${elapsed_time} seconds"