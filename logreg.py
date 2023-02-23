import pandas as pd
import numpy as np
import pickle

def load_dataset(path):
    csv = pd.read_csv(path)

    # csv = csv.drop('name', axis=1)


    # print(csv['status'].value_counts())

    y = csv.iloc[:, 0].values

    X = csv.drop(csv.columns[0], axis=1).values

    X = (X - X.min(axis=0)) / (X.max(axis=0) - X.min(axis=0))

    print("X.shape",X.shape)
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

def dataloader(total_clients, client_no):
    x, y = load_dataset('train_susy.csv')
    print(x.shape)
    print(y.shape)
    x_train, y_train = split_dataset(x, y, total_clients, client_no-1)
    print(x_train.shape)
    print(y_train.shape)

    n_attributes = x_train.shape[1]

    intercept = np.ones((x_train.shape[0], 1))
    x_train = np.concatenate((intercept, x_train), axis=1)

    return x_train, y_train, n_attributes

class LogisticRegression:
    def __init__(self, client_no, lr=0.1, n_iter=10):
        self.lr = lr
        self.n_iter = n_iter
        self.converged = False
        self.client_no = client_no
        self.x_train, self.y_train, self.n_attributes = dataloader(3, client_no)
        self.params = np.random.rand(self.n_attributes + 1)
        
    def sigmoid(self,x):
        return 1 / (1 + np.exp(-x.dot(self.params)))

    def gradient_descent(self,X,y,h):
        return np.dot(X.T, (h - y)) / y.shape[0]

    def cross_entropy(self, h):
        y = self.y_train
        return -y * np.log(h) - (1 - y) * np.log(1 - h)

    def binary_cross_entropy_loss(self,y_true, y_pred):
        
        epsilon = 1e-15  # to avoid taking the log of 0
        y_pred = np.clip(y_pred, epsilon, 1 - epsilon)  # to avoid taking the log of values too close to 0 or 1
        loss = - (y_true * np.log(y_pred) + (1 - y_true) * np.log(1 - y_pred)).mean()
        return loss
    
    def save_model(self):
        with open('model.pkl', 'wb') as f:
            pickle.dump(self, f)

    def run(self):
        h = self.sigmoid(self.x_train)
        gradient_pi = self.gradient_descent(self.x_train,self.y_train,h)
        loss_pi = self.binary_cross_entropy_loss(self.y_train,h)

        print(f"loss: {loss_pi}")
        print(f"gradient: {gradient_pi}")

        #save loss and gradient as pickle files
        with open('loss'+str(self.client_no)+'.pkl', 'wb') as f:
            pickle.dump(loss_pi, f)
        with open('gradient'+str(self.client_no)+'.pkl', 'wb') as f:
            pickle.dump(gradient_pi, f)
    
    def predict(self,x):
        h = self.sigmoid(x)
        return h        
    
    # def load_model(self):
    #     with open('model.pkl', 'rb') as f:
    #         model = pickle.load(f)
    #     return model
    
    def set_params(self, params):
        self.params = params
    
    def set_converged(self, converged):
        self.converged = converged
