from passlib.hash import pbkdf2_sha256


def pass_encryption():
    password = pbkdf2_sha256.hash()
    print(pbkdf2_sha256.verify("passwo2rd", password))
