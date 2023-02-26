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
    csv = pd.read_csv(path)

    csv = csv.drop('name', axis=1)

    # print(csv['status'].value_counts())

    y = csv['status'].values

    X = csv.drop('status', axis=1).values

    X = (X - X.min(axis=0)) / (X.max(axis=0) - X.min(axis=0))
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


client_no = client.recv(2048).decode(FORMAT)
client_no = int(client_no)
total_clients = client.recv(2048).decode(FORMAT)
total_clients = int(total_clients)
print("client_no: ", client_no)
print("total_clients: ", total_clients)

X, y = load_dataset('parkinsons.csv')
print(X.shape)
print(y.shape)
x_train, y_train = split_dataset(X, y, total_clients, client_no)
y_ = np.where(y_train <= 0, -1, 1)
print(x_train)
print(y_train.shape)

n_attributes = x_train.shape[1]

converged = False

W = client.recv(2048).decode(FORMAT)
W = np.fromstring(W[1:-1], dtype=float, sep=' ')
b = 0
print(W)

lambda_param=0.01
learning_rate=0.001

def hinge_loss(y, y_pred):
    loss = lambda_param * np.dot(W, W)
    loss += np.mean(np.maximum(0, 1 - y * y_pred))
    return loss

while not converged:
    dw = 0
    db = 0
    for idx, x_i in enumerate(x_train):
        condition = y_[idx] * (np.dot(x_i, W) - b) >= 1
        if condition:
            dw += learning_rate * (2 * lambda_param * W)
            db += 0
        else:
            dw += learning_rate * (2 * lambda_param * W - np.dot(x_i, y_[idx]))
            db += learning_rate * y_[idx]


    approx = np.dot(x_train, W) - b
    prediction = np.sign(approx)
    loss_pi = hinge_loss(y_, prediction)
    dW_pi = dw
    db_pi = db

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