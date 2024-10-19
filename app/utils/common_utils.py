import hashlib
import zlib

def get_key(full_data):
    return hashlib.sha1(full_data).hexdigest()

def get_compressed_data(full_data):
    return zlib.compress(full_data)