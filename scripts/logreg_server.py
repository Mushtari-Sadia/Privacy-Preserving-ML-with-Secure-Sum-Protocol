import pickle
import numpy as np

n_parties = 3
gradient_list = []
loss_list = []
learning_rate = 0.1
n_attributes = 18 #for susy
epsilon = 0.001


try:
    with open('params.pkl', 'rb') as f:
        params = pickle.load(f)
except:
    params = np.random.rand(n_attributes)


#load loss of 3 clients from pickle file
for i in range(1,4):
    with open('loss'+str(i)+'.pkl', 'rb') as f:
        loss_list.append(pickle.load(f))
    with open('gradient'+str(i)+'.pkl', 'rb') as f:
        gradient_list.append(pickle.load(f))

#  M computes global gradient Gj
gradient = np.sum(gradient_list, axis=0)
print(f"gradient: {gradient}")
loss_new = np.sum(loss_list)
print(f"loss: {loss_new}")


# M computes new parameters θj+1
params = params - learning_rate * gradient

# M sends { θj+1 } to all parties
# save params as pickle file
with open('params.pkl', 'wb') as f:
    pickle.dump(params, f)

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
converged = False
# if np.abs(loss_new - loss) < epsilon:
#     converged = True
#     print(f"converged: {converged}")
