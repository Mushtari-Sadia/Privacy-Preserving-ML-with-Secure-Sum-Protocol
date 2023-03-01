#installing packages in each of the containers
docker exec server pip3 install BitVector

echo "server: BitVector version"
docker exec server python3 -c "import BitVector; print(BitVector.__version__)"

for i in {1..3}; do
    docker exec client$i pip3 install BitVector

    echo "Container $i: BitVector version"
    docker exec client$i python3 -c "import BitVector; print(BitVector.__version__)"
done
