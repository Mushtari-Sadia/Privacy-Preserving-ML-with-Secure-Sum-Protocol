import pickle
from svm import *
import sys
from linreg import *

client_no = int(sys.argv[1])

#load params
try : 
    with open('params.pkl', 'rb') as f:
        params = pickle.load(f)
except :
    print("randomly initializing parameters")
    ds = Dataset()
    x,y = ds.load_dataset("train_bike.csv")
    n_attributes = x.shape[1]
    params = np.zeros(n_attributes)

try : 
    with open('bias.pkl', 'rb') as f:
        bias = pickle.load(f)
except :
    print("initializing bias with zero")
    bias = 0

model = LinearRegression(client_no=client_no,lr = 0.1)
print("params")
print(params)
model.set_params(params)
model.set_bias(bias)
model.run()