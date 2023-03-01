import pandas as pd
import numpy as np
import pickle
from dataset import *

class LogisticRegression:
    def __init__(self, client_no, lr=0.1, n_iter=10):
        self.lr = lr
        self.n_iter = n_iter
        self.converged = False
        self.client_no = client_no
        ds = Dataset()
        self.x_train, self.y_train, self.n_attributes = ds.dataloader(3, client_no,'train_susy.csv')
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
