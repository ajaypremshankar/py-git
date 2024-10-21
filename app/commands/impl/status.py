import os
from pathlib import Path

from app.commands.base import Command
from app.lib import core
from app.utils import common_utils

"""
Building intuition of `Status` Command:

So let's say file is already committed (A).
Now author made changes in the file (A').

How do we find out if these two files are same? A & A'

in simplest way,

1. Find root tree - HEAD -> commit sha -> tree
2. recursively check:
    a. if any folder/file that doesn't exist in git, mark it as untracked
    b. if file exists (by path) but sha1 doesn't match, mark it modified

Caveats:
- This approach will obv have performance issues in monorepos. I'll attempt to improve when I get to implementing diff command

"""


def is_git_ignored(git_ignored: dict[str, bool], path: str):
    for gi_key in git_ignored.keys():
        if gi_key in Path(path).parts:
            return True
    return False


def compare_flattened_trees(git_tree: dict[str, dict], working_tree: dict[str, dict]):
    git_ignored = core.get_git_ignored()
    untracked_files = {}

    for key, val in working_tree.items():
        path = key

        if (git_tree.get(path) is None
                and not is_git_ignored(git_ignored, path)):
            untracked_files[key] = val

    changed_files = {}
    deleted_files = {}
    for key, val in git_tree.items():
        path = key
        hash_key = val.get("hash")

        if working_tree.get(path) is None:
            deleted_files[key] = val
        elif working_tree.get(path).get("hash") != hash_key:
            changed_files[key] = val

    return {
        "modified": changed_files,
        "deleted": deleted_files,
        "untracked": untracked_files
    }


class StatusCommand(Command):
    def execute(self):

        last_commit = core.get_last_commit_on_current_branch()

        flattened_git_tree = self.get_flattened_git_tree(last_commit)

        flattened_working_tree = self.get_flattened_work_tree()

        comparison = compare_flattened_trees(flattened_git_tree, flattened_working_tree)

        for com_key, com_val in comparison.items():
            if com_val:
                for item in com_val.keys():
                    print(f"{com_key}: {common_utils.get_repo_path_from_abs_path(item)}")
                print("\n")

    def print_result(self):
        pass

    def get_flattened_git_tree(self,
                               tree_sha: str,
                               parent_dir: str = common_utils.get_repo_path()) -> dict[str, dict]:
        result = {}
        tree = core.ls_tree(tree_sha)

        for t in tree:
            obj_type = t.get("type")
            hash_key = t.get("hash")
            path = f"{parent_dir}/{t.get("name")}"

            if obj_type == 'tree':
                r = self.get_flattened_git_tree(hash_key, path)
                result.update(r)
            elif obj_type == 'blob':
                result[path] = t

        return result

    def get_flattened_work_tree(self, directory: str = common_utils.get_repo_path()) -> dict[str, dict]:
        result = {}

        list_dir = os.listdir(directory)

        for d in list_dir:
            if d == '.git':
                continue
            path = f"{directory}/{d}"
            if os.path.isdir(path):
                r = self.get_flattened_work_tree(path)
                result.update(r)
            elif os.path.isfile(path):
                result[path] = {
                    "type": "blob",
                    "hash": core.hash_object(path, False),
                    "name": d,
                    "mode": "100644",
                }
            else:
                raise RuntimeError(f"Failed to get {path}")

        return result
