import pandas as pd
import numpy as np
import pickle
from dataset import *

class SupportVectorMachine:
    def __init__(self, client_no, lr=0.001, n_iter=10):
        self.lr = lr
        self.n_iter = n_iter
        self.converged = False
        self.client_no = client_no
        ds = Dataset()
        self.x_train, self.y_train, self.n_attributes = ds.dataloader(3, client_no, 'train_susy.csv')
        self.y_ = np.where(self.y_train <= 0, -1, 1)
        self.W = np.random.rand(self.n_attributes + 1)
        self.bias = 0
        self.lambda_param=0.01
    
    def hinge_loss(self,y, y_pred):
        loss = self.lambda_param * np.dot(self.W, self.W)
        loss += np.mean(np.maximum(0, 1 - y * y_pred))
        return loss
        
    
    def save_model(self):
        with open('model.pkl', 'wb') as f:
            pickle.dump(self, f)

    def run(self):
        dw = 0
        db = 0
        for idx, x_i in enumerate(self.x_train):
            
            condition = self.y_[idx] * (np.dot(x_i, self.W) - self.bias) >= 1
            # check if condition type is list
            if type(condition) == list:
                condition = condition[0]
                print('idx',idx)
                print('self.y_[idx]',self.y_[idx])
                print('x_i',x_i.shape)
            if condition:
                dw += self.lr * (2 * self.lambda_param * self.W)
                db += 0
            else:
                dw += self.lr * (2 * self.lambda_param * self.W - np.dot(x_i, self.y_[idx]))
                db += self.lr * self.y_[idx]


        approx = np.dot(self.x_train, self.W) - self.bias
        prediction = np.sign(approx)
        loss_pi = self.hinge_loss(self.y_, prediction)
        dW_pi = dw
        db_pi = db

        print(f"loss: {loss_pi}")

        #save loss and gradient as pickle files
        with open('loss'+str(self.client_no)+'.pkl', 'wb') as f:
            pickle.dump(loss_pi, f)
        with open('gradient'+str(self.client_no)+'.pkl', 'wb') as f:
            pickle.dump(dW_pi, f)
        with open('dbias'+str(self.client_no)+'.pkl', 'wb') as f:
            pickle.dump(db_pi, f)
    
    def predict(self,x):
        print("x.shape",x.shape)
        print("self.W.shape",self.W.shape)
        print("self.bias.shape",self.bias.shape)
        approx = np.dot(x, self.W) - self.bias
        prediction = np.sign(approx)
        return np.where(prediction == -1, 0, 1)   
    
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
