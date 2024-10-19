from app.commands.base import Command

"""
Brainstorming Status Command:

So let's say file is already committed (A).
Now author made changes in the file (A').

How do we find out if these two files are same? A & A'

in simplest way,

1. Find root tree - HEAD -> commit sha -> tree
2. recursively check:
    a. if any folder/file that doesn't exist in git, mark it as untracked
    b. if file exists (by path) but sha1 doesn't match, mark it modified

"""

class StatusCommand(Command):
    def execute(self):
        pass

    def print_result(self):
        pass