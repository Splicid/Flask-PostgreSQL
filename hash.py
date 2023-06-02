import os, pprint
from passlib.hash import pbkdf2_sha256

env_var = os.environ
#pprint.pprint(dict(env_var), width = 1)

#print(dict(env_var))
def pass_encryption():
    password = pbkdf2_sha256.hash()
    print(pbkdf2_sha256.verify("passwo2rd", password))
