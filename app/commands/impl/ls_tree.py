from app.commands.base import Command, CommandOutput
from app.lib import core


class LsTreeCommand(Command):
    def __init__(self, args):
        args_dict = {}
        for arg in args:
            if len(arg) == 40:
                args_dict["hash"] = arg
            elif arg == '--name-only':
                args_dict["name_only"] = True

        super().__init__(args_dict)

    def execute(self):
        tree_sha = self.get_arg("hash")
        result = core.ls_tree(tree_sha)
        self.output = CommandOutput(True, "", data={
            "result": result
        })

    def print_result(self):
        for i in self.get_data("result"):
            if self.get_arg("name_only"):
                print(i.get("name"))
            else:
                print(f"{i.get("mode")} {i.get("type")} {i.get("hash")} {i.get("name")}")