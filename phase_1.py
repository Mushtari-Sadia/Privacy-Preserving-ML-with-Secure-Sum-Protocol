from rsa import *
import sys

my_client_id = sys.argv[1]
rsa = RSA(my_client_id)
rsa.generateKeys()


rsa_test_encryption = RSA()
rsa_test_encryption.setPublicKey('public0.pkl')
rsa_test_encryption.setPlainText('abcd')
rsa_test_encryption.createCipher()


rsa_test_encryption.setPrivateKey('private0.pkl')
rsa_test_encryption.decipher()
rsa_test_encryption.createDecipheredText()

print(rsa_test_encryption.decipheredtext)

