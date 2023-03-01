import pickle
from svm import *
import sys

client_no = int(sys.argv[1])

#load params
try : 
    with open('params.pkl', 'rb') as f:
        params = pickle.load(f)
except :
    print("randomly initializing parameters")
    ds = Dataset()
    x,y = ds.load_dataset("train_susy.csv")
    n_attributes = x.shape[1]
    params = np.random.randn(n_attributes)

try : 
    with open('bias.pkl', 'rb') as f:
        bias = pickle.load(f)
except :
    print("randomly initializing bias")
    bias = 0

model = SupportVectorMachine(client_no=client_no,lr = 0.00001)
print("params")
print(params)
model.set_params(params)
model.set_bias(bias)
model.run()