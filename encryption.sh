for i in {1..3}; do
    echo "Container $i: encryption started"
    #each client encrypting local file with all public keys
    docker exec client$i python phase_2.py $i
    # docker logs -f client$i

    #each client sending their own encrypted file to server
    docker exec -d server sh -c "rm encrypted${i}.pkl"
    docker exec -d server sh -c "nc -l -v -p 1234 -w 1 > encrypted${i}.pkl"
    docker exec client$i sh -c "cat encrypted${i}.pkl | nc -v server 1234"
    sleep 1

    while [ true ];do
        filesize=$(docker exec server stat -c%s encrypted${i}.pkl)
        if [ $filesize -eq 0 ]; then
            echo "Container $i: sending encrypted${i}.pkl failed, retrying"
            docker exec -d server sh -c "nc -l -v -p 1234 -w 1 > encrypted${i}.pkl"
            docker exec client$i sh -c "cat encrypted${i}.pkl | nc -v server 1234"
            sleep 1
        else 
            echo "Container $i: sending encrypted${i}.pkl succeeded"
            break
        fi
    done

done