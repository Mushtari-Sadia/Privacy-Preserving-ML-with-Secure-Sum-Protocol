
filename=$1

docker exec -it server sh -c "rm ${filename}1.pkl"
docker exec -it server sh -c "rm ${filename}2.pkl"
docker exec -it server sh -c "rm ${filename}3.pkl"

chmod +x encryption.sh
chmod +x decryption.sh
./encryption.sh $1
./decryption.sh $1

# docker exec -it server sh -c "cat $1"
# docker exec -it server sh -c "cat $1"
# docker exec -it server sh -c "cat $1"