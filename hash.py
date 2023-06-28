import os, pprint
from passlib.hash import pbkdf2_sha256

env_var = os.environ
#pprint.pprint(dict(env_var), width = 1)

#print(dict(env_var))
def pass_encryption(db_pass):
    password = pbkdf2_sha256.hash(db_pass)
    return password 

def pass_check(db_check, user_check):
    #db_encrypt = pbkdf2_sha256.hash(db_check)
    return pbkdf2_sha256.verify(user_check, db_check)