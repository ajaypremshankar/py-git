from app.commands.base import Command

"""
Building intuition of `Commit` Command:

Limitation: While staging area is missing, we'll have to commit everything that is changed in working directory.

1. Write repo root tree recursively, gets you the root tree sha. Ignore gitignore files for commit
2. Obtain last commit. Will this become the parent commit?
3. Write commit tree using tree sha (from 1) and parent commit sha (from 2)
4. Point refs/<curr_branch> to this commit sha


Questions:
1. Should we delete files from git? If got deleted from repo
2. If new file is added to existing folder, we'll have to create new tree or can we create all trees from stratch. Ignore what already existings


"""


class CommitCommand(Command):
    def __init__(self, args):
        args_dict = {}
        index = 0
        message_at = -1

        for arg in args:
            if arg == '-m':
                message_at = index + 1

            index += 1

        if len(args) <= message_at or message_at == -1:
            raise RuntimeError("Mandatory commit message not passed")
        else:
            args_dict["message"] = args[message_at]

        super().__init__(args_dict)

    def execute(self):
        pass

    def print_result(self):
        pass
