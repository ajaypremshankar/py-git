import zlib
import os
from app.utils import file_utils, common_utils

def get_header(data, obj_type: str):
    return '{} {}'.format(obj_type, len(data)).encode()

def get_full_data(data, obj_type: str):
    return get_header(data, obj_type) + b'\x00' + data

def get_dir_file_name_from_hash(hash_key: str):
    return hash_key[:2], hash_key[2:]

def get_obj_path_from_hash(hash_key: str):
    dir_name, file_name = get_dir_file_name_from_hash(hash_key)
    return f".git/objects/{dir_name}/{file_name}"

def write_obj(hash_key: str, full_data):
    obj_file = get_obj_path_from_hash(hash_key)
    os.makedirs(os.path.dirname(obj_file), exist_ok=True)
    file_utils.write_file(obj_file, common_utils.get_compressed_data(full_data))

def read_obj(hash_key: str):
    obj_file = get_obj_path_from_hash(hash_key)
    content = file_utils.read_file(file_path=obj_file)
    return zlib.decompress(content)
