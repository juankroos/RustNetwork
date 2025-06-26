import hashlib
import io, os, sys, time, zlib
import cryptography


def hash_file(file_path):
    with open(file_path, 'rb') as f:
        hash_ = f.read()
        hash_ = hashlib.sha256(hash_).hexdigest()
        print(hash_)

if __name__ == "__main__":
    file = 'E:\RustNetwork\project\src\crypt_python\mr hero.txt'
    hash_file(file)
    #with open(file, 'rb') as f:
    #    print(f.read())
