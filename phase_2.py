# encrypt local data with all public keys
from rsa import *
import binascii
import pickle
import sys

client_id = sys.argv[1]

def process_input(filename):
        with open(filename, 'rb') as f:
            content = f.read()
        hextext = str(binascii.hexlify(content))
        hextext = hextext[2:] 
        hextext = hextext[:-1]
        print(hextext)
        return hextext


#for testing purposes,delete later
# for i in range(11):
#     rsa = RSA(i)
#     rsa.generateKeys()

#Here the filename which stores the gradient of the model is passed as input
plaintext = process_input('test.txt')

rsa_test_encryption = RSA()

#We encrypt the gradients with the public keys of all the nodes
#Serially, from mediator, client1 to client10

for i in range(11):
    print("setting public key :",i)
    rsa_test_encryption.setPublicKey('public'+str(i)+'.pkl')
    rsa_test_encryption.setPlainText(plaintext)
    rsa_test_encryption.createCipher()
    #the ciphertext is of the previous layer is the plaintext for the next layer
    plaintext = rsa_test_encryption.ciphertext

#The gradients are now encrypted with 11 layers of encryption
#store the encrypted file as a pickle file
with open('encrypted'+str(client_id)+'.pkl', 'wb') as f:
    pickle.dump(plaintext, f)

# for i in range(10,-1,-1):
#     rsa_test_encryption.setPrivateKey('private'+str(i)+'.pkl')
#     rsa_test_encryption.decipher()

#     rsa_test_encryption.ciphertext = rsa_test_encryption.decryptedtext

# rsa_test_encryption.createDecipheredText()

# create_file_from_decrypted_text(rsa_test_encryption.decipheredtext,'test.txt')
