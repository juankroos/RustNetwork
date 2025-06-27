import datetime
import hashlib
import io, os, sys, time, zlib
import cryptography

def write_file():
    file = open('hash.txt', 'w')
    entry = f"file: {file}"+"date: "+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+","+"hash: "+hash_+'\n'
    file.write(entry)
    file.close()
    # simple verification
    state = print(os.path.isfile('hash.txt'))
    if state:
        print("hash file create successfuly")
    else:
        print("let try again")
    return state
 
#simple hashing whit sha256
def hash_file(file_path):
    with open(file_path, 'rb') as f:
        hash_ = f.read()
        hash_ = hashlib.sha256(hash_).hexdigest()
        print(hash_)
        
        with open(r'./hash1.txt','r') as fi:
            entry = f"file: {file}"+"date: "+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+","+"hash: "+hash_+'\n'
            previous_state = fi.read()
            fi.close()
            with open(r'./hash1.txt','w') as fi:
                fi.write(previous_state)
                fi.write(entry)
                fi.close()


if __name__ == "__main__":
    file = 'E:\RustNetwork\project\src\crypt_python\mr hero.txt'
    #hash_file(file)
    files = open(file, 'r')
    line  = files.seek(0)
    print("###########################")
    #print(files.read())
    print(files.tell())
    for count, line in enumerate(files):
        print(f"Line {count}: {line.strip()}\n")
        
    #with open(file, 'rb') as f:
    #    print(f.read())

def insert(file_path,data, new_data):
    with open(file_path, 'a') as f:
        #content = f.read()
        for count, line in enumerate(file):
            if data in line:
                print(f'found a match line----{count}: {line.strip()}')
                # change the line
                new_line = line.replace(data, new_data)

            else:
                print('theres no match')

#hash line per line
def hash_line(src_path):
    entry = " "
    with open(src_path, 'rb') as f:
        for count, line in enumerate(f):
            hash_ = hashlib.sha256(line.encode()).hexdigest()
            entry =f' {hash_}\n + {entry}'
            with open(src_path, 'w') as f:
                f.write(entry+ '\n')

        f.close()
    print(f"hashing completed for -------- {src_path}.")
            