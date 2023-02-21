import pickle
from logreg import *
import sys

client_no = int(sys.argv[1])

#load params
try : 
    with open('params.pkl', 'rb') as f:
        params = pickle.load(f)
except :
    params = np.random.randn(23)

model = LogisticRegression(client_no=client_no)
model.set_params(params)
model.run()