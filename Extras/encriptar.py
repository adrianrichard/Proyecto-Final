##from cryptography.fernet import Fernet
##
##key = Fernet.generate_key()
##f = Fernet(key)
##token = f.encrypt(b'A really secret message. Not for prying eyes.')
##print(token)
##token=f.decrypt(token)
##print(token)


##import hashlib
##h = hashlib.sha1(b"www.recursospython.com - Recursos Python")
##print(h.digest(), h.hexdigest())

##from simplecrypt import encrypt, decrypt
##passkey = 'wow'
##str1 = 'I am okay'
##cipher = encrypt(passkey, str1)
##print(cipher)
import os
curDir = os.getcwd()
print(curDir)
