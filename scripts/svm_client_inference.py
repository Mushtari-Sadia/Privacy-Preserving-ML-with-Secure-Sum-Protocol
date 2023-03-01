import pickle
from svm import *
import sys
import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score
from dataset import *

client_no = int(sys.argv[1])
scenario = sys.argv[2]


ds = Dataset()
X,y_true = ds.load_dataset("test_susy.csv") 
n_attributes = X.shape[1]

#load params
try : 
    with open('params.pkl', 'rb') as f:
        params = pickle.load(f)
except :
    print("could not load params")
    params = np.random.randn(n_attributes)

try : 
    with open('bias.pkl', 'rb') as f:
        bias = pickle.load(f)
except :
    print("could not load params")
    bias = 0

params = params[:18]

model = SupportVectorMachine(client_no=client_no,lr = 0.00001)
model.set_params(params)
model.set_bias(bias)
y_pred = model.predict(X)
# for i in range(len(y_pred)):
#     print(y_pred[i])
print(y_pred)
print(y_true)

# y_pred[y_pred > 0.8] = 1
# y_pred[y_pred <= 0.8] = 0

accuracy = accuracy_score(y_true, y_pred)
precision = precision_score(y_true, y_pred)
recall = recall_score(y_true, y_pred)

#store values in a text file
with open(scenario+'_metrics'+str(client_no)+'.txt', 'a') as f:
    f.write("SVM : Accuracy for client "+str(client_no)+": "+str(accuracy)+"\n")
    f.write("SVM : Precision for client "+str(client_no)+": "+str(precision)+"\n")
    f.write("SVM : Recall for client "+str(client_no)+": "+str(recall)+"\n")

print("SVM : Accuracy for client",client_no,": ",accuracy)
print("SVM : Precision for client",client_no,": ",precision)
print("SVM : Recall for client",client_no,": ",recall)
