from cryptography.fernet import Fernet
import numpy as np
from array import array

key = Fernet.generate_key()
f = Fernet(key)
token = f.encrypt(b"secret")
print(f.decrypt(token))

##
with open(r'E:\RustNetwork\project\src\crypt_python\mr hero.txt', 'w') as f:
    f.write(key.decode())

fernet = Fernet(key)

with open(r'E:\RustNetwork\project\src\crypt_python\nba.csv', 'rb') as f:
    original = f.read()

encrypted = fernet.encrypt(original)

with open(r'E:\RustNetwork\project\src\crypt_python\nba_encrypted.csv', 'wb') as f:
    f.write(encrypted)

#simple encryption too simple 
def enc_file():
    input1 = "juan"
    lib = 'abcdefghijklmnopqrstuvwxyz'
    new_input = np.array([])
    key = 2
    count = 0
    for i in input1:
        for j in lib:
            if i == j:
                index = lib.index(j) + key % len(lib)
                value = lib[index]
                new_input = np.append(value, new_input)
                print(f"the index of {i} is {index} and the count is {lib.index(j)}...blabla {value}")
                #count +=0
    #a = ' '.join(new_input)
    print(f"the new input is {a}")

if __name__ == "__main__":
    enc_file()
   