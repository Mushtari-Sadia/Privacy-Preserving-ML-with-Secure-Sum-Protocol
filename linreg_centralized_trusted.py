# Importing libraries

import numpy as np
import pandas as pd
from sklearn.metrics import r2_score
from dataset import *

def mean_absolute_error(y_true, y_pred):
    return np.mean(np.abs(y_true - y_pred))

def mean_squared_error(y_true, y_pred):
    return np.mean((y_true - y_pred) ** 2)

def root_mean_squared_error(y_true, y_pred):
    return np.sqrt(mean_squared_error(y_true, y_pred))

# Linear Regression

class LinearRegression():

    def __init__(self, learning_rate, iterations):
        self.learning_rate = learning_rate

        self.iterations = iterations

    # Function for model training

    def fit(self, X, Y):
        # no_of_training_examples, no_of_features

        self.m, self.n = X.shape

        # weight initialization

        self.W = np.zeros(self.n)

        self.b = 0

        self.X = X

        self.Y = Y

        # gradient descent learning

        for i in range(self.iterations):
            # print("===========================Iteration: {}".format(i + 1))
            self.update_weights()

        return self

    # Helper function to update weights in gradient descent

    def update_weights(self):
        Y_pred = self.predict(self.X)
        print("Y_pred: {}".format(Y_pred))
        loss_pi = mean_squared_error(self.Y, Y_pred)
        
        print("Loss: {}".format(loss_pi))
        # print mean squared error, mean absolute error, root mean squared error
        # print("MSE: {}".format(mean_squared_error(self.Y, Y_pred)))
        # print("MAE: {}".format(mean_absolute_error(self.Y, Y_pred)))
        # print("RMSE: {}".format(root_mean_squared_error(self.Y, Y_pred)))

        # calculate gradients

        dW = - (2 * (self.X.T).dot(self.Y - Y_pred)) / self.m

        db = - 2 * np.sum(self.Y - Y_pred) / self.m

        print("dW: {}".format(dW))
        print("db: {}".format(db))

        # update weights

        self.W = self.W - self.learning_rate * dW

        self.b = self.b - self.learning_rate * db

        return self

    # Hypothetical function h( x )

    def predict(self, X):
        return X.dot(self.W) + self.b


# driver code

def main():
    # Importing dataset
    ds = Dataset()
    # data load
    X, y = ds.load_dataset('train_bike.csv')
    # print(X.shape, y.shape)

    # split train and test
    # X_train, y_train, X_test, y_test = split_dataset(X, y, 0.2, shuffle=True)
    # print(X_train.shape, y_train.shape, X_test.shape, y_test.shape)

    X_train, y_train = X, y
    X_test, y_test = ds.load_dataset('test_bike.csv')

    print(X_train.shape)
    print(X_test.shape)
    print(y_train.shape)
    print(y_test.shape)

    # Model training

    model = LinearRegression(iterations=10, learning_rate=0.1)

    model.fit(X_train, y_train)

    # Prediction on test set

    Y_pred = model.predict(X_test)
    print(Y_pred)
    print(y_test)

    #print mean squared error, mean absolute error, root mean squared error for test set
    # print("=========================================Test set")
    print("R2: {}".format(r2_score(y_test, Y_pred)))
    print("MSE: {}".format(mean_squared_error(y_test, Y_pred)))
    print("MAE: {}".format(mean_absolute_error(y_test, Y_pred)))
    print("RMSE: {}".format(root_mean_squared_error(y_test, Y_pred)))



if __name__ == "__main__":
    main()
