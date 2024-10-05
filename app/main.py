import sys
import os
import zlib

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
            raw = read_file(f".git/objects/{dir}/{file_name}")
            header, content = raw.split(b"\0", maxsplit=1)
            print(content.decode("utf-8"), end="", sep="")
    else:
        raise RuntimeError(f"Unknown command #{command}")


def read_file(file_path: str):
    with open(file_path, "rb") as file:
        content = zlib.decompress(file.read())
    return content

if __name__ == "__main__":
    main()
