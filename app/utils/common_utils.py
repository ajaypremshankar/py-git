import hashlib
import os
import zlib

def get_key(full_data):
    return hashlib.sha1(full_data).hexdigest()

def get_compressed_data(full_data):
    return zlib.compress(full_data)

def get_repo_path(sub_path: str = None):
    if sub_path:
        return f"{os.getcwd()}/{sub_path}"
    else:
        return os.getcwd()

def is_repo_path(sub_path):
    path = f"{os.getcwd()}/{sub_path}"
    return os.path.isfile(path) or os.path.isfile(path)

def get_repo_path_from_abs_path(abs_path: str):
    repo_path = abs_path.replace(get_repo_path(), "")

    return repo_path[1:] if repo_path.startswith("/") else repo_path