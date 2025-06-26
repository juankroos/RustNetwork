import os
import datetime

def DeleteFile(file_path):
    try:
        os.remove(file_path)
        return True
    except OSError as e:
        print(f"Error deleting file {file_path}: {e}")
        return False
    
def Copy_file(file_path):
    try:
        with open(file_path, 'rb') as f:
            copy = f.read()
        return copy
    except OSError as e:
        print(f"error copying file {file_path}: {e}")
        if os.path.exists(file_path):
            print(f"File {file_path} exists but could not be read.")
        else:            
            print(f"File {file_path} does not exist.")
        return None
    
def Move_file(src_path, dest_path):
    try:
        os.rename(src_path, dest_path)
        return True
    except OSError as e:
        print(f"Error moving file from {src_path} to {dest_path}: {e}")
        if os.path.exists(src_path):
            print(f"Source file {src_path} exists but could not be moved.")
        else:
            print(f"Source file {src_path} does not exist.")
        return False


def Rename(src_path, new_name):
    try:
        if  os.path.isfile(new_name):
            print("the file already exists")
        else:
            os.rename(src_path, new_name)
            print(f'file modified successfully',+'date :'+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    except OSError as e:
        print(f"Error renaming file {src_path} to {new_name}: {e}")
        if os.path.exists(src_path):
            print(f"Source file {src_path} exists but could not be renamed.")
        else:
            print(f"Source file {src_path} does not exist.")
        return False

        
