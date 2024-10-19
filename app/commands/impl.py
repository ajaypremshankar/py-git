import os
import sys
from abc import ABC, abstractmethod

from app.lib import core
from app.utils import object_utils

repo_path = os.getcwd()

class CommandOutput:
    def __init__(self, status: bool,
                 message: str = "",
                 data: dict = None):
        self.status = status
        self.data = data
        self.message = message
        self.output = None

class Command(ABC):
    """
    Abstract base class for Command objects.
    Concrete commands must implement the 'execute' method.
    """

    def __init__(self, args):
        self.args = args
        self.output = None

    @abstractmethod
    def execute(self):
        """
        Execute the command.
        """
        pass

    @abstractmethod
    def print_result(self):
        """
        Execute the command.
        """
        pass

    def get_data(self, key: str):
        return self.output.data.get(key, None)

    def execution_result(self):
        return self.output

    def is_success(self):
        return self.output.status


class InitCommand(Command):

    def __init__(self, args):
        super().__init__(args)

    def execute(self):
        os.mkdir(f"{repo_path}/.git")
        os.mkdir(f"{repo_path}/.git/objects")
        os.mkdir(f"{repo_path}/.git/refs")
        with open(f"{repo_path}/.git/HEAD", "w") as f:
            f.write("ref: refs/heads/main\n")

        self.output = CommandOutput(True)

    def print_result(self):
        if self.is_success():
            print("Initialized git directory")
        else:
            print("Failed int git directory")


class CatFileCommand(Command):

    def __init__(self, args):
        super().__init__(args)

    def execute(self):
        if self.args[1] == "-p":
            hash_key = super().args[2]
            raw = object_utils.read_obj(hash_key)
            header, content = raw.split(b"\0", maxsplit=1)
            self.output = CommandOutput(True, "", data={
                "header": header,
                "content": content
            })
        else:
            self.output = CommandOutput(False, "Command Not Supported yet. Pass -p arg.")

    def print_result(self):
        content = self.get_data("content")
        print(content.decode("utf-8"), end="", sep="")


class HashObjectCommand(Command):
    def execute(self):
        hash_key = core.hash_object(super().args[2], True)
        self.output = CommandOutput(True, "", {
            "hash_key": hash_key
        })

    def print_result(self):
        hash_key = self.get_data("hash_key")
        sys.stdout.write(f"{hash_key}")


class LsTree(Command):
    def execute(self):
        tree_sha = self.args[2]
        name_only = True if len(self.args) > 2 and self.args[3] == '--name-only' else False
        result = core.ls_tree(tree_sha, name_only)
        self.output = CommandOutput(True, "", data={
            "result": result
        })

    def print_result(self):
        for i in self.get_data("result"):
            print(i.name.decode())


class WriteTreeCommand(Command):
    def execute(self):
        hash_key = core.write_dir_as_tree(repo_path)
        self.output = CommandOutput(True, "", {
            "hash_key": hash_key
        })

    def print_result(self):
        hash_key = self.get_data("hash_key")
        sys.stdout.write(f"{hash_key}")


class CommitTreeCommand(Command):
    def execute(self):
        hash_key = core.commit_tree(self.args)
        self.output = CommandOutput(True, "", {
            "hash_key": hash_key
        })

    def print_result(self):
        hash_key = self.get_data("hash_key")
        sys.stdout.write(f"{hash_key}")
