import pickle
from logreg import *
import sys
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score
from dataset import *

ds = Dataset()

client_no = int(sys.argv[1])
scenario = sys.argv[2]


X,y_true = ds.load_dataset("test_susy.csv")
n_attributes = X.shape[1]

#load params
try : 
    with open('params.pkl', 'rb') as f:
        params = pickle.load(f)
except :
    print("could not load params")
    params = np.random.randn(n_attributes+1)

params = params[:n_attributes]

model = LogisticRegression(client_no=client_no)
model.set_params(params)
y_pred = model.predict(X)
# for i in range(len(y_pred)):
#     print(y_pred[i])
print(y_pred)
print(y_true)

y_pred[y_pred > 0.8] = 1
y_pred[y_pred <= 0.8] = 0

accuracy = accuracy_score(y_true, y_pred)
precision = precision_score(y_true, y_pred)
recall = recall_score(y_true, y_pred)

#store values in a text file
with open(scenario+'_metrics'+str(client_no)+'.txt', 'a') as f:
    f.write("Accuracy for client "+str(client_no)+": "+str(accuracy)+"\n")
    f.write("Precision for client "+str(client_no)+": "+str(precision)+"\n")
    f.write("Recall for client "+str(client_no)+": "+str(recall)+"\n")

print("LOGREG: Accuracy for client",client_no,": ",accuracy)
print("LOGREG: Precision for client",client_no,": ",precision)
print("LOGREG: Recall for client",client_no,": ",recall)
