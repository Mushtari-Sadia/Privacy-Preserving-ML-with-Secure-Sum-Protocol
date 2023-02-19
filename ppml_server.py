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

n_parties = 3
gradient_list = []
loss_list = []

# M initializes { θ1, · · · , θn }
n_attributes = 22
params = np.random.rand(n_attributes + 1)
learning_rate = 0.01
epsilon = 0.001

# M sets convergence to false, M sets J to ∞
converged = False
# loss = np.inf

def handle_client(conn, addr, params, loss, gradient_list, loss_list, client_no, total_clients):
    print(f"[NEW CONNECTION] {addr} connected.")

    conn.send(str(client_no).encode(FORMAT))
    conn.send(str(total_clients).encode(FORMAT))

    # M sends { θ1, . . . , θn } to all parties
    conn.send(str(params).encode(FORMAT))

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
        gradient_pi = np.fromstring(msg[1:-1], dtype=float, sep=' ')
        gradient_list.append(gradient_pi)

        # M computes global gradient Gj
        while len(gradient_list) < n_parties:
            pass

        gradient = np.sum(gradient_list, axis=0)
        print(f"gradient: {gradient}")
        loss_new = np.sum(loss_list)
        print(f"loss: {loss_new}")

        #clear lists
        sleep(0.1)
        gradient_list.clear()
        loss_list.clear()

        # M computes new parameters θj+1
        params = params - learning_rate * gradient

        # M sends { θj+1 } to all parties
        conn.send(str(params).encode(FORMAT))

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
        thread = threading.Thread(target=handle_client, args=(conn, addr, params, np.inf, gradient_list, loss_list, client_no, n_parties))
        client_no += 1
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


print("[STARTING] server is starting...")
print(f"Server IP: {SERVER}")
start()