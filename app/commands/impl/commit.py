from app.commands.base import Command

"""
Building intuition of `Commit` Command:

Limitation: While staging area is missing we'll have to commit everything that is changed in working directory.

1. Write repo root tree recursively, gets you the root tree sha
2. Obtain last commit. Will this become the parent commit?
3. Write commit tree using tree sha (from 1) and parent commit sha (from 2)


Questions:
1. Should we delete files from git? If got deleted from repo



"""


class CommitCommand(Command):
    def execute(self):
        pass

    def print_result(self):
        pass