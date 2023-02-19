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

def sigmoid(x, params):
    return 1 / (1 + np.exp(-x.dot(params)))

def gradient_descent(X, h, y):
    return np.dot(X.T, (h - y)) / y.shape[0]

def cross_entropy(y, h):
    return -y * np.log(h) - (1 - y) * np.log(1 - h)

def binary_cross_entropy_loss(y_true, y_pred):
    epsilon = 1e-15  # to avoid taking the log of 0
    y_pred = np.clip(y_pred, epsilon, 1 - epsilon)  # to avoid taking the log of values too close to 0 or 1
    loss = - (y_true * np.log(y_pred) + (1 - y_true) * np.log(1 - y_pred)).mean()
    return loss

client_no = client.recv(2048).decode(FORMAT)
client_no = int(client_no)
total_clients = client.recv(2048).decode(FORMAT)
total_clients = int(total_clients)
print("client_no: ", client_no)
print("total_clients: ", total_clients)

x, y = load_dataset('parkinsons.csv')
print(x.shape)
print(y.shape)
x_train, y_train = split_dataset(x, y, total_clients, client_no)
print(x_train.shape)
print(y_train.shape)

n_attributes = x_train.shape[1]

intercept = np.ones((x_train.shape[0], 1))
x_train = np.concatenate((intercept, x_train), axis=1)

converged = False

params = client.recv(2048).decode(FORMAT)
params = np.fromstring(params[1:-1], dtype=float, sep=' ')
# params = np.random.rand(n_attributes+1)
print(params)

while not converged:
    h = sigmoid(x_train, params)
    gradient_pi = gradient_descent(x_train, h, y_train)
    loss_pi = binary_cross_entropy_loss(y_train, h)

    print(f"loss: {loss_pi}")
    print(f"gradient: {gradient_pi}")

    client.send(str(loss_pi).encode(FORMAT))
    # wait for server to finish updating
    sleep(0.1)
    client.send(str(gradient_pi).encode(FORMAT))

    params = client.recv(2048).decode(FORMAT)
    params = np.fromstring(params[1:-1], dtype=float, sep=' ')
    print(params)

    msg = client.recv(2048).decode(FORMAT)
    print(f"converged: {msg}")
    converged = True if msg == 'True' else False

send(DISCONNECT_MESSAGE)