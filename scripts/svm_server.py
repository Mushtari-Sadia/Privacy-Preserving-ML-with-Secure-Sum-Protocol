import pickle
import numpy as np

n_parties = 3
gradient_list = []
loss_list = []
bias_list = []
learning_rate = 0.00001
n_attributes = 18 #for susy
epsilon = 0.001


try:
    with open('params.pkl', 'rb') as f:
        params = pickle.load(f)
except:
    params = np.random.rand(n_attributes)

try:
    with open('bias.pkl', 'rb') as f:
        bias = pickle.load(f)
except:
    bias = 0


#load loss of 3 clients from pickle file
for i in range(1,4):
    with open('loss'+str(i)+'.pkl', 'rb') as f:
        loss_list.append(pickle.load(f))
    with open('gradient'+str(i)+'.pkl', 'rb') as f:
        gradient_list.append(pickle.load(f))
    with open('dbias'+str(i)+'.pkl', 'rb') as f:
        bias_list.append(pickle.load(f))

#  M computes global gradient Gj
gradient = np.sum(gradient_list, axis=0)
print(f"gradient: {gradient}")
dbias = np.sum(bias_list, axis=0)
print(f"bias: {dbias}")
loss_new = np.sum(loss_list)
print(f"loss: {loss_new}")


# M computes new parameters θj+1
print("gradient shape",gradient.shape)
print("params shape",params.shape)
params = params - learning_rate * gradient
bias = bias - learning_rate * dbias

# M sends { θj+1 } to all parties
# save params as pickle file
with open('params.pkl', 'wb') as f:
    pickle.dump(params, f)
with open('bias.pkl', 'wb') as f:
    pickle.dump(bias, f)

# load loss file from pickle
try:
    with open('loss_old.pkl', 'rb') as f:
        loss = pickle.load(f)
except:
    loss = np.inf
# save loss new as pickle file
with open('loss_old.pkl', 'wb') as f:
    pickle.dump(loss_new, f)



# M computes convergence
# converged = False
# if np.abs(loss_new - loss) < epsilon:
#     converged = True
#     print(f"converged: {converged}")
