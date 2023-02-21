import os
import sys
import pickle
from rsa import *

client_id = sys.argv[1]

# def create_file_from_decrypted_text(decipher,filename):
#     data = bytes.fromhex(decipher)
#     name = filename.split('/')[-1]
#     os.makedirs("received/", exist_ok=True)
#     with open("received/"+name, 'wb') as file:
#         file.write(data)

rsa_test_decryption = RSA()
rsa_test_decryption.setPrivateKey('private'+str(client_id)+'.pkl')

for i in range(1,4):
    with open('encrypted'+str(i)+'.pkl', 'rb') as f:
        print("decrypting file from client =",i)
        rsa_test_decryption.ciphertext = pickle.load(f)
        #strip off one layer of encryption
        rsa_test_decryption.decipher()
        #store the decrypted file with the same name
        with open('encrypted'+str(i)+'.pkl', 'wb') as f:
            pickle.dump(rsa_test_decryption.decryptedtext, f)


