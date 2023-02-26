import socket
import threading
from time import sleep

import numpy as np

HEADER = 2048
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

n_parties = 2
dW_list = []
db_list = []
loss_list = []

# M initializes { θ1, · · · , θn }
n_attributes = 11
W = np.random.rand(n_attributes)
b = 0
learning_rate = 0.01
epsilon = 0.001

# M sets convergence to false, M sets J to ∞
converged = False
# loss = np.inf

def handle_client(conn, addr, W, b, loss, dW_list, db_list, loss_list, client_no, total_clients):
    print(f"[NEW CONNECTION] {addr} connected.")

    conn.send(str(client_no).encode(FORMAT))
    conn.send(str(total_clients).encode(FORMAT))

    # M sends { θ1, . . . , θn } to all parties
    conn.send(str(W).encode(FORMAT))

    connected = True
    while connected:
        # M receives {E[{LJi }1], E[{LJi }2], E[{LGi1 }1], E[{LGi1 }2],· · · , E[{LGin }1], E[{LGin }2]} from all Pi
        msg = conn.recv(HEADER).decode(FORMAT)

        if msg == DISCONNECT_MESSAGE:
            connected = False
            print(f"[{addr}] {msg}")
            continue
        # conn.send("Msg received".encode(FORMAT))
        print(f"[{addr}] {msg}")

        loss_pi = float(msg)
        loss_list.append(loss_pi)

        msg = conn.recv(HEADER).decode(FORMAT)
        dW_pi = np.fromstring(msg[1:-1], dtype=float, sep=' ')
        dW_list.append(dW_pi)

        msg = conn.recv(HEADER).decode(FORMAT)
        db_pi = float(msg)
        db_list.append(db_pi)

        # M computes global gradient Gj
        while len(dW_list) < n_parties:
            pass

        dW = np.mean(dW_list, axis=0)
        db = np.sum(db_list)
        print(f"dW: {dW}")
        print(f"db: {db}")
        loss_new = np.mean(loss_list)
        print(f"loss: {loss_new}")

        #clear lists
        sleep(0.01)
        dW_list.clear()
        db_list.clear()
        loss_list.clear()

        # M computes new parameters θj+1
        W = W - learning_rate * dW
        b = b - learning_rate * db

        # M sends { θj+1 } to all parties
        conn.send(str(W).encode(FORMAT))
        conn.send(str(b).encode(FORMAT))

        sleep(0.01)

        # M computes convergence
        converged = False
        if np.abs(loss_new - loss) < epsilon:
            converged = True
            print(f"converged: {converged}")
        conn.send(str(converged).encode(FORMAT))
        print(f"converged: {converged}")
        loss = loss_new



    conn.close()


def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    client_no = 0
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr, W, b, np.inf, dW_list, db_list, loss_list, client_no, n_parties))
        client_no += 1
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


print("[STARTING] server is starting...")
print(f"Server IP: {SERVER}")
start()