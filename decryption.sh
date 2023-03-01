filename=$1

# server sending all encrypted files to client 3
for i in {1..3}; do
        echo "Container 3: receiving encrypted${i}.pkl from server"
        docker exec -d client3 sh -c "rm encrypted${i}.pkl"
        docker exec -d client3 sh -c "nc -l -p 1234 -w 10 > encrypted${i}.pkl"
        docker exec server sh -c "cat encrypted${i}.pkl | nc -v client3 1234"
done

for i in {3..2}; do
    # client stripping off one layer of encryption
    echo "Container $i: decryption started"
    docker exec client$i python phase_3.py $i
    sleep 2
    echo "Container $i: decryption finished"
    echo "Container $i: sending files to client $((i-1))"
    # send all files to next client
    for j in {1..3}; do
        docker exec -d client$((i-1)) sh -c "rm encrypted${j}.pkl"
        docker exec -d client$((i-1)) sh -c "nc -l -v -p 1234 -w 10 > encrypted${j}.pkl"
        docker exec client$i sh -c "cat encrypted${j}.pkl | nc -v client$((i-1)) 1234"
        echo "Container $i: sent encrypted${j}.pkl to client $((i-1))"
        sleep 1

        while [ true ];do
            filesize=$(docker exec client$((i-1)) stat -c%s encrypted${j}.pkl)
            if [ $filesize -eq 0 ]; then
                echo "Container $i: sending encrypted${j}.pkl failed, retrying"
                docker exec -d client$((i-1)) sh -c "nc -l -v -p 1234 -w 10 > encrypted${j}.pkl"
                docker exec client$i sh -c "cat encrypted${j}.pkl | nc -v client$((i-1)) 1234"
                sleep 1
            else 
                echo "Container $i: sending encrypted${j}.pkl succeeded"
                break
            fi
        done
    done


    echo -e "\n\n"
done

# client 1 stripping off one layer of encryption
docker exec -d client1 python phase_3.py 1
echo "Container 1: decryption finished"
# send all files to server
for j in {1..3}; do
    docker exec -d server sh -c "rm encrypted${j}.pkl"
    docker exec -d server sh -c "nc -l -p 1234 -w 10 > encrypted${j}.pkl"
    docker exec client1 sh -c "cat encrypted${j}.pkl | nc -v server 1234"
    echo "Container 1: sent encrypted${j}.pkl to server"
    sleep 1

    while [ true ];do
        filesize=$(docker exec server stat -c%s encrypted${j}.pkl)
        if [ $filesize -eq 0 ]; then
            echo "Container 1: sending encrypted${j}.pkl failed, retrying"
            docker exec -d server sh -c "nc -l -p 1234 -w 10 > encrypted${j}.pkl"
            docker exec client1 sh -c "cat encrypted${j}.pkl | nc -v server 1234"
            sleep 1
        else 
            echo "Container 1: sending encrypted${j}.pkl succeeded"
            break
        fi
    done

done

# server stripping off final layer of encryption
docker exec server python phase_3.py 0
docker exec server python phase_4.py $filename
