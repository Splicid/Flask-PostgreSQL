from passlib.hash import pbkdf2_sha256

# testing hashing with passlib

password = pbkdf2_sha256.hash("password")

print(pbkdf2_sha256.verify("passwo2rd", password))
