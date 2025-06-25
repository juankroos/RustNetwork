from cryptography.fernet import Fernet

key = Fernet.generate_key()
f = Fernet(key)
token = f.encrypt(b"secret")
print(f.decrypt(token))

##
with open('filekey.key', 'wb') as f:
    f.write(key)