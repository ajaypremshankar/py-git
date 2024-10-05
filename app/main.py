import sys
import os
import zlib
import hashlib

def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    # print("Logs from your program will appear here!")

    # Uncomment this block to pass the first stage
    
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
            hash = sys.argv[3]
            dir = hash[:2]
            file_name = hash[2:]
            raw = read_file_decompressed(f".git/objects/{dir}/{file_name}")
            header, content = raw.split(b"\0", maxsplit=1)
            print(content.decode("utf-8"), end="", sep="")
    elif command == 'hash-object':
        handle_hash_object(argv=sys.argv)
    else:
        raise RuntimeError(f"Unknown command #{command}")


def handle_hash_object(argv: list[str]):
    if sys.argv[2] == '-w':
        raw = read_file(sys.argv[3])
        header = f"blob {len(raw)}\x00"
        result = header.encode("ascii") + raw

        sha1 = hashlib.sha1()
        sha1.update(result)
        hex = sha1.hexdigest()

        dir = hex[:2]
        file_name = hex[2:]

        os.makedirs(os.path.dirname(f".git/objects/{dir}/{file_name}"), exist_ok=True)
        write_file(f".git/objects/{dir}/{file_name}", zlib.compress(result))

        sys.stdout.write(f"{hex}")


def read_file_decompressed(file_path: str):
    content = read_file(file_path)
    return zlib.decompress(content)


def read_file(file_path: str):
    with open(file_path, "rb") as file:
        return file.read()

def write_file(file_path: str, data):
    with open(file_path, "wb") as file:
        return file.write(data)

if __name__ == "__main__":
    main()
