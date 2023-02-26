from time import sleep

import pandas as pd
import numpy as np
import socket

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "10.18.96.100"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    client.send(message)
    print(f"[{ADDR}] {message}")

def load_dataset(path):
    df = pd.read_csv(path)

    X = df.iloc[:, :-1].values

    y = df.iloc[:, 1].values
    return X, y


def split_dataset(X, y, n_partition, pi, shuffle=False):
    if shuffle:
        indices = np.random.permutation(X.shape[0])
    else:
        indices = np.arange(X.shape[0])

    # partition the data to n_partition and take the pi-th partition as training set
    partition_size = int(X.shape[0] / n_partition)
    training_idx = indices[pi * partition_size: (pi + 1) * partition_size]
    X_train, y_train = X[training_idx, :], y[training_idx]

    return X_train, y_train

def mean_absolute_error(y_true, y_pred):
    return np.mean(np.abs(y_true - y_pred))

def mean_squared_error(y_true, y_pred):
    return np.mean((y_true - y_pred) ** 2)

def root_mean_squared_error(y_true, y_pred):
    return np.sqrt(mean_squared_error(y_true, y_pred))

client_no = client.recv(2048).decode(FORMAT)
client_no = int(client_no)
total_clients = client.recv(2048).decode(FORMAT)
total_clients = int(total_clients)
print("client_no: ", client_no)
print("total_clients: ", total_clients)

x, y = load_dataset('bike.csv')
print(x.shape)
print(y.shape)
x_train, y_train = split_dataset(x, y, total_clients, client_no)
print(x_train.shape)
print(y_train.shape)

n_attributes = x_train.shape[1]

converged = False

W = client.recv(2048).decode(FORMAT)
W = np.fromstring(W[1:-1], dtype=float, sep=' ')
b = 0
# W = np.random.rand(n_attributes+1)
print(W)

while not converged:
    y_pred = x_train.dot(W) + b
    loss_pi = mean_squared_error(y_train, y_pred)

    dW_pi = - (2 * (x_train.T).dot(y_train - y_pred)) / x_train.shape[0]

    db_pi = - 2 * np.sum(y_train - y_pred) / x_train.shape[0]

    print(f"loss: {loss_pi}")
    # print(f"gradient: {gradient_pi}")

    client.send(str(loss_pi).encode(FORMAT))
    # wait for server to finish updating
    sleep(0.1)
    client.send(str(dW_pi).encode(FORMAT))
    client.send(str(db_pi).encode(FORMAT))

    W = client.recv(2048).decode(FORMAT)
    W = np.fromstring(W[1:-1], dtype=float, sep=' ')
    print(W)

    b = client.recv(2048).decode(FORMAT)
    b = float(b)
    print(b)

    msg = client.recv(2048).decode(FORMAT)
    print(f"converged: {msg}")
    converged = True if msg == 'True' else False

send(DISCONNECT_MESSAGE)