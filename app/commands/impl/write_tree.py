import sys

from app.commands.base import Command, CommandOutput
from app.lib import core
from app.utils import common_utils


class WriteTreeCommand(Command):
    def execute(self):
        hash_key = core.write_dir_as_tree(common_utils.get_repo_path())
        self.output = CommandOutput(True, "", {
            "hash_key": hash_key
        })

    def print_result(self):
        hash_key = self.get_data("hash_key")
        sys.stdout.write(f"{hash_key}")
