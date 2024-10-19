import sys

from app.commands.base import Command, CommandOutput
from app.lib import core


class CommitTreeCommand(Command):
    def execute(self):
        hash_key = core.commit_tree(self.args)
        self.output = CommandOutput(True, "", {
            "hash_key": hash_key
        })

    def print_result(self):
        hash_key = self.get_data("hash_key")
        sys.stdout.write(f"{hash_key}")
