import sys
import os
import zlib
import hashlib

class FileUtils:
    @staticmethod
    def read_file(file_path: str):
        with open(file_path, "rb") as file:
            return file.read()

    @staticmethod
    def write_file(file_path: str, data):
        with open(file_path, "wb") as file:
            return file.write(data)

class ObjectUtils:

    @staticmethod
    def get_header(data, obj_type: str):
        return '{} {}'.format(obj_type, len(data)).encode()

    @staticmethod
    def get_full_data(data, obj_type: str):
        return ObjectUtils.get_header(data, obj_type) + b'\x00' + data

    @staticmethod
    def get_dir_file_name_from_hash(hash_key: str):
        return hash_key[:2], hash_key[2:]

    @staticmethod
    def get_obj_path_from_hash(hash_key: str):
        dir_name, file_name = ObjectUtils.get_dir_file_name_from_hash(hash_key)
        return f".git/objects/{dir_name}/{file_name}"

    @staticmethod
    def write_obj(hash_key: str, full_data):
        obj_file = ObjectUtils.get_obj_path_from_hash(hash_key)
        os.makedirs(os.path.dirname(obj_file), exist_ok=True)
        FileUtils.write_file(obj_file, CommonUtils.get_compressed_data(full_data))

    @staticmethod
    def read_obj(hash_key: str):
        obj_file = ObjectUtils.get_obj_path_from_hash(hash_key)
        content = FileUtils.read_file(file_path=obj_file)
        return zlib.decompress(content)


class CommonUtils:
    @staticmethod
    def get_key(full_data):
        return hashlib.sha1(full_data).hexdigest()

    @staticmethod
    def get_compressed_data(full_data):
        return zlib.compress(full_data)

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
            raw = ObjectUtils.read_obj(hash_key)
            header, content = raw.split(b"\0", maxsplit=1)
            print(content.decode("utf-8"), end="", sep="")
    elif command == 'hash-object':
        hash_key = hash_object(sys.argv[3], True)
        sys.stdout.write(f"{hash_key}")
    elif command == 'ls-tree':
        ls_tree(argv=sys.argv)
    elif command == 'write-tree':
        hash_key = write_dir_as_tree(".")
        sys.stdout.write(f"{hash_key}")
    else:
        raise RuntimeError(f"Unknown command #{command}")

def write_dir_as_tree(path: str):
    if path == './.git':
        return ""
    tree_nodes = []

    contents = sorted(
        os.listdir(path),
        key=lambda x: x if os.path.isfile(os.path.join(path, x)) else f"{x}/",
    )

    for content in contents:
        content_path = f"{path}/{content}"
        if os.path.isdir(content_path):
            tree_hash = write_dir_as_tree(content_path)
            tree_nodes.append({
                'hash': tree_hash,
                'type': 'tree',
                'mode': 40000,
                'name': content
            })
        else:
            hash_key = hash_object(content_path, True)
            tree_nodes.append({
                'hash': hash_key,
                'type': 'blob',
                'mode': 100644,
                'name': content
            })


    byte_content = bytearray()
    for tree_node in tree_nodes:
        if not tree_node.get("hash", "") == "":
            byte_content += f"{tree_node.get("mode")} {tree_node.get("name", "")}\0".encode()
            byte_content += int.to_bytes(int(tree_node.get("hash"), base=16), length=20, byteorder="big")

    full_data = ObjectUtils.get_full_data(byte_content, 'tree')

    sha_key = CommonUtils.get_key(full_data)

    ObjectUtils.write_obj(sha_key, full_data)

    return sha_key

def hash_object(path: str, is_write = True):
    if is_write:
        raw = FileUtils.read_file(path)
        full_data = ObjectUtils.get_full_data(raw, 'blob')

        sha_key = CommonUtils.get_key(full_data)

        ObjectUtils.write_obj(sha_key, full_data)
        return sha_key

def ls_tree(argv: list[str]):
    if argv[2] == '--name-only':
        tree_sha = argv[3]

        tree_content = ObjectUtils.read_obj(tree_sha)
        _, binary_data = tree_content.split(b"\x00", maxsplit=1)

        while binary_data:
            mode, binary_data = binary_data.split(b"\x00", maxsplit=1)
            _, name = mode.split()
            binary_data = binary_data[20:]
            print(name.decode())

if __name__ == "__main__":
    main()
