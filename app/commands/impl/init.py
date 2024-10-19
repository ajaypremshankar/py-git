import os

from app.commands.base import Command, CommandOutput
from app.utils import common_utils

class InitCommand(Command):
    def __init__(self, args):
        super().__init__(args)

    def execute(self):
        os.mkdir(common_utils.get_repo_path(".git"))
        os.mkdir(common_utils.get_repo_path(".git/objects"))
        os.mkdir(common_utils.get_repo_path(".git/refs"))
        with open(common_utils.get_repo_path(".git/HEAD"), "w") as f:
            f.write("ref: refs/heads/main\n")

        self.output = CommandOutput(True)

    def print_result(self):
        if self.is_success():
            print("Initialized git directory")
        else:
            print("Failed int git directory")
