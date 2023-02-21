# for i in {1..3}; do
#     docker exec client$i sh -c "python ppml_client.py $i" &
# done
docker exec client1 sh -c "python ppml_client.py 1" &
docker exec server sh -c "python ppml_server.py" &
jobs