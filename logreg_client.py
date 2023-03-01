import pickle
from logreg import *
import sys
from dataset import *

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

model = LogisticRegression(client_no=client_no)
print("params")
print(params)
model.set_params(params)
model.run()