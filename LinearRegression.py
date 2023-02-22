# Importing libraries

import numpy as np

import pandas as pd

def split_dataset(X, y, test_size=0.2, shuffle=True):
    if shuffle:
        indices = np.random.permutation(X.shape[0])
    else:
        indices = np.arange(X.shape[0])

    # print(indices)
    training_count = int(X.shape[0] * (1 - test_size))

    training_idx, test_idx = indices[:training_count], indices[training_count:]

    X_train, y_train, X_test, y_test = X[training_idx, :], y[training_idx], X[test_idx, :], y[test_idx]
    return X_train, y_train, X_test, y_test

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
            print("===========================Iteration: {}".format(i + 1))
            self.update_weights()

        return self

    # Helper function to update weights in gradient descent

    def update_weights(self):
        Y_pred = self.predict(self.X)

        # print mean squared error, mean absolute error, root mean squared error
        print("MSE: {}".format(mean_squared_error(self.Y, Y_pred)))
        print("MAE: {}".format(mean_absolute_error(self.Y, Y_pred)))
        print("RMSE: {}".format(root_mean_squared_error(self.Y, Y_pred)))

        # calculate gradients

        dW = - (2 * (self.X.T).dot(self.Y - Y_pred)) / self.m

        db = - 2 * np.sum(self.Y - Y_pred) / self.m

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

    df = pd.read_csv("bike.csv")

    X = df.iloc[:, :-1].values

    Y = df.iloc[:, 1].values

    # Splitting dataset into train and test set

    X_train, Y_train, X_test,  Y_test = split_dataset(X, Y, 0.2)

    print(X_train.shape)
    print(X_test.shape)
    print(Y_train.shape)
    print(Y_test.shape)

    # Model training

    model = LinearRegression(iterations=1000, learning_rate=0.01)

    model.fit(X_train, Y_train)

    # Prediction on test set

    Y_pred = model.predict(X_test)

    #print mean squared error, mean absolute error, root mean squared error for test set
    print("=========================================Test set")
    print("MSE: {}".format(mean_squared_error(Y_test, Y_pred)))
    print("MAE: {}".format(mean_absolute_error(Y_test, Y_pred)))
    print("RMSE: {}".format(root_mean_squared_error(Y_test, Y_pred)))



if __name__ == "__main__":
    main()
