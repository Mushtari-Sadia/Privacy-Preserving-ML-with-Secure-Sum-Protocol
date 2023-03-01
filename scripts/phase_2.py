# encrypt local data with all public keys
from rsa import *
import binascii
import pickle
import sys

client_id = sys.argv[1]
filename = sys.argv[2]

def process_input(filename):
    with open(filename, 'rb') as f:
        content = f.read()
    hextext = str(binascii.hexlify(content))
    hextext = hextext[2:] 
    hextext = hextext[:-1]
    print(hextext)
    return hextext


#Here the filename which stores the gradient of the model is passed as input
plaintext = process_input(filename+client_id+'.pkl')

rsa_test_encryption = RSA()

#We encrypt the gradients with the public keys of all the nodes
#Serially, from mediator, client1 to client3

for i in range(4):
    print("setting public key :",i)
    rsa_test_encryption.setPublicKey('public'+str(i)+'.pkl')
    rsa_test_encryption.setPlainText(plaintext)
    rsa_test_encryption.createCipher()
    #the ciphertext is of the previous layer is the plaintext for the next layer
    plaintext = rsa_test_encryption.ciphertext

#The gradients are now encrypted with 4 layers of encryption
#store the encrypted file as a pickle file
with open('encrypted'+str(client_id)+'.pkl', 'wb') as f:
    pickle.dump(plaintext, f)

