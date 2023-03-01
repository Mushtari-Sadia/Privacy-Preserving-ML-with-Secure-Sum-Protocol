import pickle
from linreg import *
import sys
import numpy as np
from dataset import *
from sklearn.metrics import r2_score

def mean_absolute_error(y_true, y_pred):
    return np.mean(np.abs(y_true - y_pred))

def mean_squared_error(y_true, y_pred):
    return np.mean((y_true - y_pred) ** 2)

def root_mean_squared_error(y_true, y_pred):
    return np.sqrt(mean_squared_error(y_true, y_pred))


client_no = int(sys.argv[1])
scenario = sys.argv[2]

ds = Dataset()
X,y_true = ds.load_dataset("test_bike.csv")
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

# params = params[:10]

model = LinearRegression(client_no=client_no,lr = 0.1)
model.set_params(params)
model.set_bias(bias)
y_pred = model.predict(X)
# for i in range(len(y_pred)):
#     print(y_pred[i])
print(y_pred)
print(y_true)

# y_pred[y_pred > 0.8] = 1
# y_pred[y_pred <= 0.8] = 0

mse = mean_squared_error(y_true, y_pred)
mae = mean_absolute_error(y_true, y_pred)
rmse = root_mean_squared_error(y_true, y_pred)
r2 = r2_score(y_true, y_pred)


#store values in a text file
with open(scenario+'_metrics'+str(client_no)+'.txt', 'a') as f:
    f.write("LINREG : R2: {}".format(r2))
    f.write("LINREG : MSE: {}".format(mse))
    f.write("LINREG : MAE: {}".format(mae))
    f.write("LINREG : RMSE: {}".format(rmse))


print("LINREG : R2: {}".format(r2))
print("LINREG : MSE: {}".format(mse))
print("LINREG : MAE: {}".format(mae))
print("LINREG : RMSE: {}".format(rmse))
