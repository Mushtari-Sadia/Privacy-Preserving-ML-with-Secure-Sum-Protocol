CONTAINER_NAME=server
if docker inspect --format '{{.State.Status}}' "$CONTAINER_NAME" | grep -q "running"; then
    echo ""
else
    chmod +x restart-containers.sh
    ./restart-containers.sh
fi



docker exec -it server sh -c "cd received; rm decrypted1.txt"
docker exec -it server sh -c "cd received; rm decrypted2.txt"
docker exec -it server sh -c "cd received; rm decrypted3.txt"

chmod +x encryption.sh
chmod +x decryption.sh
./encryption.sh
./decryption.sh

docker exec -it server sh -c "cd received; cat decrypted1.txt"
docker exec -it server sh -c "cd received; cat decrypted2.txt"
docker exec -it server sh -c "cd received; cat decrypted3.txt"