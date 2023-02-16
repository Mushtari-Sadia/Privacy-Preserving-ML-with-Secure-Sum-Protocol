#installing packages in each of the containers

for i in {1..10}; do
    docker exec client$i pip install BitVector

    echo "Container $i: BitVector version"
    docker exec client$i python3 -c "import BitVector; print(BitVector.__version__)"
done
