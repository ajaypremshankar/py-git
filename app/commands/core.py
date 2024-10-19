from app.commands.impl import *

def get_command(command_str: str, args):
    match command_str:
        case "init":
            return InitCommand(args)
        case "cat-file":
            return CatFileCommand(args)
        case 'hash-object':
            return HashObjectCommand(args)
        case 'write-tree':
            return WriteTreeCommand(args)
        case 'commit-tree':
            return CommitTreeCommand(args)

    raise RuntimeError(f"Unknown command #{command_str}")
