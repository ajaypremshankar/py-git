import sys

from app.commands.base import Command, CommandOutput
from app.lib import core
from app.utils import common_utils


class HashObjectCommand(Command):
    def __init__(self, args):
        args_dict = {}
        for arg in args:
            if common_utils.is_repo_path(arg):
                args_dict["path"] = arg
            elif arg == '-w':
                args_dict["write"] = True

        super().__init__(args_dict)

    def execute(self):
        hash_key = core.hash_object(self.get_arg("path"), self.get_arg("write"))
        self.output = CommandOutput(True, "", {
            "hash_key": hash_key
        })

    def print_result(self):
        hash_key = self.get_data("hash_key")
        sys.stdout.write(f"{hash_key}")
