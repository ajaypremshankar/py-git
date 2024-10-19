import os
from app.utils import file_utils, object_utils, common_utils

def hash_object(path: str, is_write = True):
    raw = file_utils.read_file(path)
    full_data = object_utils.get_full_data(raw, 'blob')

    sha_key = common_utils.get_key(full_data)

    if is_write:
        object_utils.write_obj(sha_key, full_data)
    return sha_key

def write_dir_as_tree(path: str):
    if path == f"{path}/.git":
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
            byte_content += f"{tree_node.get("mode")} {tree_node.get("name")}\0".encode()
            byte_content += int.to_bytes(int(tree_node.get("hash"), base=16), length=20, byteorder="big")

    full_data = object_utils.get_full_data(byte_content, 'tree')

    sha_key = common_utils.get_key(full_data)

    object_utils.write_obj(sha_key, full_data)

    return sha_key

def ls_tree(tree_sha: str):

    result = []

    tree_content = object_utils.read_obj(tree_sha)
    _, binary_data = tree_content.split(b"\x00", maxsplit=1)

    while binary_data:
        mode_and_name, binary_data = binary_data.split(b"\x00", maxsplit=1)
        mode, name = mode_and_name.split()
        int_byte = binary_data[:20]
        binary_data = binary_data[20:]
        hash_key = hex(int.from_bytes(int_byte, byteorder="big"))[2:].zfill(40)

        result.append({
            "name": name.decode(),
            "mode": mode.decode(),
            "hash": hash_key,
            "type": "tree" if mode.decode() == '40000' else "blob"
        })
    return result


def commit_tree(args: list[str]):
    tree_sha = args[1]
    commit = args[3]
    message = args[5]

    commit_obj = bytearray()
    commit_obj += f"tree {tree_sha}\n".encode()
    commit_obj += f"parent {commit}\n".encode()
    commit_obj += f"author ajay <ajay@test.com>\n\n".encode()
    commit_obj += f"{message}\n".encode()

    full_data = object_utils.get_full_data(commit_obj, 'commit')
    sha_key = common_utils.get_key(full_data)

    object_utils.write_obj(sha_key, full_data)

    return sha_key
