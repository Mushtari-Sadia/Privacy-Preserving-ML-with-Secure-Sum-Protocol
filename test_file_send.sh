docker cp "$(pwd)/test_file_send.txt" client5:test_file_send.txt
docker exec -d client6 sh -c "nc -l -p 1234 -w 10 > test_file_send.txt"
docker exec -d client5 sh -c "cat test_file_send.txt | ncclient6 1234"
# docker logs -f client5
# docker logs -f client6