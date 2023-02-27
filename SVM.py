import datasets as datasets
import numpy as np
import pandas as pd
from sklearn import datasets
from sklearn.model_selection import train_test_split

accuracy_list = []
loss_list = []

def accuracy(y_true, y_pred):
    accuracy = np.sum(y_true==y_pred) / len(y_true)
    return accuracy
def precision(y_true, y_pred):
    tp = np.sum(y_true * y_pred)
    fp = np.sum((1-y_true) * y_pred)
    # tn = np.sum((1-y_true) * (1-y_pred))
    # fn = np.sum(y_true * (1-y_pred))
    #
    # print("tn: ", tn)
    # print("fn: ", fn)
    # print("fp: ", fp)
    # print("tp: ", tp)

    if tp == 0:
        # print("tp is 0")
        return 0

    return tp / (tp + fp)
def recall(y_true, y_pred):
    tp = np.sum(y_true * y_pred)
    fn = np.sum(y_true * (1-y_pred))
    # print("fn: ", fn)

    if tp == 0:
        # print("tp is 0")
        return 0
    return tp / (tp + fn)
def f1_score(y_true, y_pred):
    p = precision(y_true, y_pred)
    r = recall(y_true, y_pred)

    if p == 0 or r == 0:
        # print("p or r is 0")
        return 0
    return 2*p*r / (p+r)

def load_dataset(path):
    """
    function for reading data from csv
    and processing to return a 2D feature matrix and a vector of class
    :return:
    """
    csv = pd.read_csv(path)

    # csv = csv.drop('name', axis=1)
    #
    # # print(csv['status'].value_counts())
    #
    # y = csv['status'].values
    #
    # X = csv.drop('status', axis=1).values

    #take the first column as the class
    y = csv.iloc[:, 0].values
    #take the rest of the columns as the features
    X = csv.iloc[:, 1:].values

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

    def __init__(self, learning_rate=0.0001, lambda_param=0.01, n_iters=1000):
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
            # print("Hinge Loss: ", self.hinge_loss(y_, prediction))

            prediction = np.where(prediction == -1, 0, 1)
            # print("Accuracy: ", accuracy(y, prediction))

            accuracy_list.append(accuracy(y, prediction))
            loss_list.append(self.hinge_loss(y_, prediction))
            print("Accuracy: ", accuracy(y, prediction))
            print("Precision: ", precision(y, prediction))
            print("Recall: ", recall(y, prediction))
            print("F1 Score: ", f1_score(y, prediction))


    def predict(self, X):
        approx = np.dot(X, self.w) - self.b
        prediction =  np.sign(approx)
        return np.where(prediction == -1, 0, 1)

    def hinge_loss(self, y, y_pred):
        loss = self.lambda_param * np.dot(self.w, self.w)
        loss += np.mean(np.maximum(0, 1 - y * y_pred))
        return loss



X, y = load_dataset('train_susy.csv')

X_train, y_train, X_test,  y_test = split_dataset(X, y, test_size=0.2, shuffle=True)

print("X_train: ", X_train.shape)
print("X_test: ", X_test.shape)
print("y_train: ", y_train.shape)
print("y_test: ", y_test.shape)


clf = SVM(n_iters=100)
clf.fit(X_train, y_train)
predictions = clf.predict(X_test)
print("predictions: ", predictions)
print("y_test: ", y_test)



print("SVM Accuracy: ", accuracy(y_test, predictions))
print("SVM Precision: ", precision(y_test, predictions))
print("SVM Recall: ", recall(y_test, predictions))
print("SVM F1 Score: ", f1_score(y_test, predictions))

import matplotlib.pyplot as plt

#plotting the accuracy
plt.plot(accuracy_list)
plt.xlabel('Iterations')
plt.ylabel('Accuracy')
plt.title('Accuracy vs Iterations')
plt.show()

#plotting the loss
plt.plot(loss_list)
plt.xlabel('Iterations')
plt.ylabel('Loss')
plt.title('Loss vs Iterations')
plt.show()