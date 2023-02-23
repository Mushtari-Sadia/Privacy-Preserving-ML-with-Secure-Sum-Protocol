import pickle
from logreg import *
import sys

client_no = int(sys.argv[1])

#load params
try : 
    with open('params.pkl', 'rb') as f:
        params = pickle.load(f)
except :
    print("randomly initializing parameters")
    params = np.random.randn(19)

model = LogisticRegression(client_no=client_no)
print("params")
print(params)
model.set_params(params)
model.run()