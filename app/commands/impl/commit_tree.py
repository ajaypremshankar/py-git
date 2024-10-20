import sys

from app.commands.base import Command, CommandOutput
from app.utils import object_utils, common_utils


class CommitTreeCommand(Command):
    def __init__(self, args):
        args_dict = {}
        index = 0
        message_at = -1

        for arg in args:

            # TODO can be rewritten better by using any arg-parse library
            if len(arg) == 40:
                if args_dict["path"] is not None:
                    args_dict["hash"] = arg
                else:
                    args_dict["commit"] = arg
            elif arg == '-m':
                message_at = index + 1

            index += 1

        if len(args) <= message_at or message_at == -1:
            raise RuntimeError("commit message not passed")
        else:
            args_dict["message"] = args[message_at]

        super().__init__(args_dict)

    def execute(self):
        hash_key = self.commit_tree()
        self.output = CommandOutput(True, "", {
            "hash_key": hash_key
        })

    def print_result(self):
        hash_key = self.get_data("hash_key")
        sys.stdout.write(f"{hash_key}")

    def commit_tree(self):
        tree_sha = self.get_arg("hash")
        commit = self.get_arg("commit")
        message = self.get_arg("message")

        commit_obj = bytearray()
        commit_obj += f"tree {tree_sha}\n".encode()
        commit_obj += f"parent {commit}\n".encode()
        commit_obj += f"author ajay <ajay@test.com>\n\n".encode()
        commit_obj += f"{message}\n".encode()

        full_data = object_utils.get_full_data(commit_obj, 'commit')
        sha_key = common_utils.get_key(full_data)

        object_utils.write_obj(sha_key, full_data)

        return sha_key
