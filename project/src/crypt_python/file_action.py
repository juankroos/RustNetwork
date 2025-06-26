import os

def DeleteFile(file_path):
    try:
        os.remove(file_path)
        return True
    except OSError as e:
        print(f"Error deleting file {file_path}: {e}")
        return False