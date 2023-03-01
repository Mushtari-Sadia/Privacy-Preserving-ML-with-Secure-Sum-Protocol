import os
import sys
import pickle
from rsa import *

filename = sys.argv[1]

def create_file_from_decrypted_text(decipher,filename):
    data = bytes.fromhex(decipher)
    name = filename.split('/')[-1]
    # os.makedirs("received/", exist_ok=True)
    with open(name, 'wb') as file:
        file.write(data)

rsa_test_decryption = RSA()

for i in range(1,4):
    with open('encrypted'+str(i)+'.pkl', 'rb') as f:
        print("decrypting file from client =",i)
        rsa_test_decryption.decryptedtext = pickle.load(f)
        #strip off one layer of encryption
        rsa_test_decryption.createDecipheredText()
        #store the decrypted file with the same name
        create_file_from_decrypted_text(rsa_test_decryption.decipheredtext,filename+str(i)+'.pkl')


