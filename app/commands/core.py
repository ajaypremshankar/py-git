from app.commands.impl.init import InitCommand
from app.commands.impl.cat_file import CatFileCommand
from app.commands.impl.commit_tree import CommitTreeCommand
from app.commands.impl.hash_object import HashObjectCommand
from app.commands.impl.ls_tree import LsTreeCommand
from app.commands.impl.status import StatusCommand
from app.commands.impl.write_tree import WriteTreeCommand


def get_command(command_str: str, args):
    match command_str:
        case "init":
            return InitCommand(args)
        case "cat-file":
            return CatFileCommand(args)
        case 'hash-object':
            return HashObjectCommand(args)
        case 'ls-tree':
            return LsTreeCommand(args)
        case 'write-tree':
            return WriteTreeCommand(args)
        case 'commit-tree':
            return CommitTreeCommand(args)
        case'status':
            return StatusCommand(args)

    raise RuntimeError(f"Unknown command #{command_str}")
