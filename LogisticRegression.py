import numpy as np
import pandas as pd
import time
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

def accuracy(y_true, y_pred):
    """

    :param y_true:
    :param y_pred:
    :return:
    """
    accuracy = (y_true == y_pred).sum() / y_pred.shape[0]
    return accuracy

def precision_score(y_true, y_pred):
    """

    :param y_true:
    :param y_pred:
    :return:
    """
    precision = (y_true * y_pred).sum() / y_pred.sum()
    return precision


def recall_score(y_true, y_pred):
    """

    :param y_true:
    :param y_pred:
    :return:
    """
    recall = (y_true * y_pred).sum() / y_true.sum()
    return recall


def f1_score(y_true, y_pred):
    """

    :param y_true:
    :param y_pred:
    :return:
    """
    f1 = 2 * precision_score(y_true, y_pred) * recall_score(y_true, y_pred) / (
            precision_score(y_true, y_pred) + recall_score(y_true, y_pred))
    return f1

class LogisticRegression:
    def __init__(self, params):
        """
        figure out necessary params to take as input
        :param params:
        """
        # todo: implement
        self.params = params

    def sigmoid(self, X):
        z = np.dot(X, self.params)
        return 1 / (1 + np.exp(-z))

    def gradient_descent(self, X, h, y):
        return np.dot(X.T, (h - y)) / y.shape[0]

    def update_weight_loss(self, learning_rate, gradient):
        return self.params - learning_rate * gradient

    def cross_entropy(self, y, h):
        return -y * np.log(h) - (1 - y) * np.log(1 - h)

    def fit(self, X, y, num_iter=10000, learning_rate=0.01):
        """
        :param X:
        :param y:
        :return: self
        """
        assert X.shape[0] == y.shape[0]
        assert len(X.shape) == 2
        # todo: implement
        intercept = np.ones((X.shape[0], 1))
        X = np.concatenate((intercept, X), axis=1)

        start_time = time.time()
        # print("Parameters: {}".format(self.params))
        for i in range(num_iter):
            h = self.sigmoid(X)
            gradient = self.gradient_descent(X, h, y)
            self.params = self.update_weight_loss(learning_rate, gradient)

            y_pred = np.where(h >= 0.5, 1, 0)

            print("===================================================Iteration: {}".format(i + 1))
            print(f'h: {h[:10]}')
            print(f'Y_pred: {y_pred[:10]}')
            print("Loss: {}".format(self.cross_entropy(y, h).mean()))
            print('Accuracy ', accuracy(y_true=y, y_pred=y_pred))
            print('Recall score ', recall_score(y_true=y, y_pred=y_pred))
            print('Precision score ', precision_score(y_true=y, y_pred=y_pred))
            print('F1 score ', f1_score(y_true=y, y_pred=y_pred))

    def predict(self, X):
        """
        function for predicting labels of for all datapoint in X
        :param X:
        :return:
        """
        # todo: implement
        intercept = np.ones((X.shape[0], 1))
        X = np.concatenate((intercept, X), axis=1)

        result = self.sigmoid(X)
        # print(result)
        pred = np.where(result >= 0.5, 1, 0)
        return pred

if __name__ == '__main__':
    # data load
    X, y = load_dataset('train_parkinsons.csv')
    # print(X.shape, y.shape)

    # split train and test
    # X_train, y_train, X_test, y_test = split_dataset(X, y, 0.2, shuffle=True)
    # print(X_train.shape, y_train.shape, X_test.shape, y_test.shape)

    X_train, y_train = X, y
    X_test, y_test = load_dataset('test_parkinsons.csv')

    # training
    params = np.random.rand(X_train.shape[1]+1)

    # print(params.shape)
    # print(X_train.shape)
    assert len(X_train.shape) == 2

    classifier = LogisticRegression(params)
    classifier.fit(X_train, y_train, 10, 0.1)

    # testing
    y_pred = classifier.predict(X_test)
    # print(y_pred)

    # # performance on test set
    print('===================================================Performance on test set')
    print('Accuracy ', accuracy(y_true=y_test, y_pred=y_pred))
    print('Recall score ', recall_score(y_true=y_test, y_pred=y_pred))
    print('Precision score ', precision_score(y_true=y_test, y_pred=y_pred))
    print('F1 score ', f1_score(y_true=y_test, y_pred=y_pred))
