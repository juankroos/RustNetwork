from cryptography.fernet import Fernet

with open('filekey.key', 'rb') as f:
    key = f.read()

fernet = Fernet(key)

with open('nba.csv', 'rb') as f:
    encrypted = f.read()

decrypted = fernet.decrypt(encrypted)

with open('nba.csv', 'rb') as f:
    f.write(decrypted)

