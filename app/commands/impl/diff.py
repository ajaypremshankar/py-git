from app.commands.base import Command

"""
Building intuition of  `Diff` Command:

Basic implementation should be simple.

Diff basically would pick contents of files:
1. In git records
2. In working directory

Compare it using `Myers diff algorithm`

Show the results in +, - or Keep format

Heavy lifting of diff command will be done by implementing Myers algorithm.
Rest we logic from status command to find affected files and apply diff algo on it.
 

"""

class DiffCommand(Command):
    def execute(self):
        pass

    def print_result(self):
        pass