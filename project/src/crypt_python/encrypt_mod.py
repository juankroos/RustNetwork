from cryptography.fernet import Fernet

key = Fernet.generate_key()
f = Fernet(key)
token = f.encrypt(b"secret")
print(f.decrypt(token))

##
with open('filekey.key', 'rb') as f:
    f.write(key)

fernet = Fernet(key)

with open('nba.csv', 'rb') as f:
    original = f.read()

encrypted = fernet.encrypt(original)

with open('nba_encrypted.csv', 'wb') as f:
    f.write(encrypted)