import pandas as pd
import numpy as np
import pickle
from dataset import *


def mean_squared_error(y_true, y_pred):
    return np.mean((y_true - y_pred) ** 2)

class LinearRegression:
    def __init__(self, client_no, lr=0.1, n_iter=10):
        self.lr = lr
        self.n_iter = n_iter
        self.converged = False
        self.client_no = client_no
        ds = Dataset()
        self.x_train, self.y_train, self.n_attributes = ds.dataloader(3, client_no,'train_bike.csv')
        self.W = np.zeros(self.n_attributes + 1)
        self.bias = 0
    
    def save_model(self):
        with open('model.pkl', 'wb') as f:
            pickle.dump(self, f)

    def run(self):
        y_pred = self.x_train.dot(self.W) + self.bias
        # print("y_pred",y_pred)
        # print("self.y_train",self.y_train)
        loss_pi = mean_squared_error(self.y_train, y_pred)

        dW_pi = - (2 * (self.x_train.T).dot(self.y_train - y_pred)) / self.x_train.shape[0]

        db_pi = - 2 * np.sum(self.y_train - y_pred) / self.x_train.shape[0]


        # print(f"loss: {loss_pi}")
        # print(f"dW: {dW_pi}")
        # print(f"db: {db_pi}")

        #save loss and gradient as pickle files
        with open('loss'+str(self.client_no)+'.pkl', 'wb') as f:
            pickle.dump(loss_pi, f)
        with open('gradient'+str(self.client_no)+'.pkl', 'wb') as f:
            pickle.dump(dW_pi, f)
        with open('dbias'+str(self.client_no)+'.pkl', 'wb') as f:
            pickle.dump(db_pi, f)
    
    def predict(self,x):
        # print("x.shape",x.shape)
        # print("self.W.shape",self.W.shape)
        # print("self.bias.shape",self.bias.shape)
              
        y_pred = x.dot(self.W) + self.bias 
        return y_pred
    
    # def load_model(self):
    #     with open('model.pkl', 'rb') as f:
    #         model = pickle.load(f)
    #     return model
    
    def set_params(self, params):
        self.W = params
    
    def set_bias(self, bias):
        self.bias = bias
    
    def set_converged(self, converged):
        self.converged = converged
