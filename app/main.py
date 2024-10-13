import sys
import os
import zlib
import hashlib

def main():
    command = sys.argv[1]
    if command == "init":
        os.mkdir(".git")
        os.mkdir(".git/objects")
        os.mkdir(".git/refs")
        with open(".git/HEAD", "w") as f:
            f.write("ref: refs/heads/main\n")
        print("Initialized git directory")
    elif command == 'cat-file':
        if sys.argv[2] == "-p":
            hash_key = sys.argv[3]
            raw = read_obj(hash_key)
            header, content = raw.split(b"\0", maxsplit=1)
            print(content.decode("utf-8"), end="", sep="")
    elif command == 'hash-object':
        hash_object(argv=sys.argv)
    elif command == 'ls-tree':
        ls_tree(argv=sys.argv)
    else:
        raise RuntimeError(f"Unknown command #{command}")

def get_dir_file_name_from_hash(hash_key: str):
    return hash_key[:2], hash_key[2:]

def get_obj_path_from_hash(hash_key: str):
    dir_name, file_name = get_dir_file_name_from_hash(hash_key)
    return f".git/objects/{dir_name}/{file_name}"

def read_file(file_path: str):
    with open(file_path, "rb") as file:
        return file.read()

def write_file(file_path: str, data):
    with open(file_path, "wb") as file:
        return file.write(data)

def get_header(data, obj_type: str):
    return '{} {}'.format(obj_type, len(data)).encode()

def get_full_data(data, obj_type: str):
    return get_header(data, obj_type) + b'\x00' + data

def get_key(full_data):
    return hashlib.sha1(full_data).hexdigest()

def get_compressed_data(full_data):
    return zlib.compress(full_data)

def write_obj(hash_key: str, full_data):
    obj_file = get_obj_path_from_hash(hash_key)
    os.makedirs(os.path.dirname(obj_file), exist_ok=True)
    write_file(obj_file, get_compressed_data(full_data))

def read_obj(hash_key: str):
    obj_file = get_obj_path_from_hash(hash_key)
    content = read_file(obj_file)
    return zlib.decompress(content)

def hash_object(argv: list[str]):
    if sys.argv[2] == '-w':
        raw = read_file(sys.argv[3])
        full_data = get_full_data(raw, 'blob')

        sha_key = get_key(full_data)

        write_obj(sha_key, full_data)
        sys.stdout.write(f"{sha_key}")

def ls_tree(argv: list[str]):
    if sys.argv[2] == '--name-only':
        tree_sha = sys.argv[3]

        tree_content = read_obj(tree_sha)
        _, binary_data = tree_content.split(b"\x00", maxsplit=1)

        while binary_data:
            mode, binary_data = binary_data.split(b"\x00", maxsplit=1)
            _, name = mode.split()
            binary_data = binary_data[20:]
            print(name.decode())


if __name__ == "__main__":
    main()