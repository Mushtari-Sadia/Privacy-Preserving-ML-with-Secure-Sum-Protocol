import pandas as pd
import numpy as np

class Dataset:
    def load_dataset(self,path):
        if 'bike' in path:
            df = pd.read_csv(path)
            y = df['cnt'].values
            X = df.drop(columns=['cnt']).values
            X = (X - X.min(axis=0)) / (X.max(axis=0) - X.min(axis=0))
            y = (y - y.min(axis=0)) / (y.max(axis=0) - y.min(axis=0))
            print("X.shape",X.shape)
            return X, y
    
        elif 'susy' in path:
            df = pd.read_csv(path)
            y = df.iloc[:, 0].values
            X = df.drop(df.columns[0], axis=1).values
            X = (X - X.min(axis=0)) / (X.max(axis=0) - X.min(axis=0))
            print("X.shape",X.shape)
            return X, y


    def split_dataset(self,X, y, n_partition, pi, shuffle=False):
        if shuffle:
            indices = np.random.permutation(X.shape[0])
        else:
            indices = np.arange(X.shape[0])
        # partition the data to n_partition and take the pi-th partition as training set
        partition_size = int(X.shape[0] / n_partition)
        training_idx = indices[pi * partition_size: (pi + 1) * partition_size]
        X_train, y_train = X[training_idx, :], y[training_idx]

        return X_train, y_train

    def dataloader(self,total_clients, client_no, path):
        x, y = self.load_dataset(path)
        print(x.shape)
        print(y.shape)
        x_train, y_train = self.split_dataset(x, y, total_clients, client_no-1)
        print(x_train.shape)
        print(y_train.shape)
        n_attributes = x_train.shape[1]

        return x_train, y_train, n_attributes