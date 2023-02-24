import datasets as datasets
import numpy as np
import pandas as pd
from sklearn import datasets
from sklearn.model_selection import train_test_split

def load_dataset(path):
    """
    function for reading data from csv
    and processing to return a 2D feature matrix and a vector of class
    :return:
    """
    csv = pd.read_csv(path)

    csv = csv.drop('name', axis=1)

    # print(csv['status'].value_counts())

    y = csv['status'].values

    X = csv.drop('status', axis=1).values

    X = (X - X.min(axis=0)) / (X.max(axis=0) - X.min(axis=0))
    return X, y


def split_dataset(X, y, test_size=0.2, shuffle=True):
    """
    function for spliting dataset into train and test
    :param X:
    :param y:
    :param float test_size: the proportion of the dataset to include in the test split
    :param bool shuffle: whether to shuffle the data before splitting
    :return:
    """
    # todo: implement.
    if shuffle:
        indices = np.random.permutation(X.shape[0])
    else:
        indices = np.arange(X.shape[0])

    # print(indices)
    training_count = int(X.shape[0] * (1 - test_size))

    training_idx, test_idx = indices[:training_count], indices[training_count:]

    X_train, y_train, X_test, y_test = X[training_idx, :], y[training_idx], X[test_idx, :], y[test_idx]
    return X_train, y_train, X_test, y_test

class SVM:

    def __init__(self, learning_rate=0.01, lambda_param=0.01, n_iters=1000):
        self.lr = learning_rate
        self.lambda_param = lambda_param
        self.n_iters = n_iters
        self.w = None
        self.b = None


    def fit(self, X, y):
        n_samples, n_features = X.shape

        y_ = np.where(y <= 0, -1, 1)

        self.w = np.random.rand(n_features)
        self.b = 0

        for _ in range(self.n_iters):
            dw = 0
            db = 0
            for idx, x_i in enumerate(X):
                condition = y_[idx] * (np.dot(x_i, self.w) - self.b) >= 1
                if condition:
                    dw += self.lr * (2 * self.lambda_param * self.w)
                    db += 0
                else:
                    dw += self.lr * (2 * self.lambda_param * self.w - np.dot(x_i, y_[idx]))
                    db += self.lr * y_[idx]

            self.w -= dw
            self.b -= db

            approx = np.dot(X, self.w) - self.b
            prediction = np.sign(approx)
            print("Hinge Loss: ", self.hinge_loss(y_, prediction))


    def predict(self, X):
        approx = np.dot(X, self.w) - self.b
        prediction =  np.sign(approx)
        return np.where(prediction == -1, 0, 1)

    # np.mean([max(0, 1 - x * y) for x, y in zip(new_actual, new_predicted)])
    def hinge_loss(self, y, y_pred):
        return np.mean([max(0, 1 - x * y) for x, y in zip(y, y_pred)])

X, y = load_dataset('parkinsons.csv')

X_train, y_train, X_test,  y_test = split_dataset(X, y, test_size=0.2, shuffle=True)

print("X_train: ", X_train.shape)
print("X_test: ", X_test.shape)
print("y_train: ", y_train.shape)
print("y_test: ", y_test.shape)


clf = SVM(n_iters=1000)
clf.fit(X_train, y_train)
predictions = clf.predict(X_test)
print("predictions: ", predictions)
print("y_test: ", y_test)

def accuracy(y_true, y_pred):
    accuracy = np.sum(y_true==y_pred) / len(y_true)
    return accuracy

print("SVM Accuracy: ", accuracy(y_test, predictions))