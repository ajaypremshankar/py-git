from app.commands.base import CommandOutput, Command
from app.utils import object_utils

class CatFileCommand(Command):
    def __init__(self, args):
        args_dict = {}
        for arg in args:
            if len(arg) > 7:
                args_dict["hash"] = arg
            elif arg == '-p':
                args_dict["pretty_print"] = True

        super().__init__(args_dict)

    def execute(self):
        hash_key = self.get_arg("hash")
        raw = object_utils.read_obj(hash_key)
        header, binary_data = raw.split(b"\0", maxsplit=1)

        result = []

        while binary_data:
            mode_and_name, binary_data = binary_data.split(b"\x00", maxsplit=1)
            mode, name = mode_and_name.split()
            int_byte = binary_data[:20]
            binary_data = binary_data[20:]
            hash_key = hex(int.from_bytes(int_byte, byteorder="big"))[2:].zfill(40)

            result.append({
                "name": name.decode(),
                "mode": mode.decode(),
                "hash": hash_key,
                "type": "tree" if mode.decode() == '40000' else "blob"
            })

        self.output = CommandOutput(True, "", data={
            "header": header,
            "content": result
        })

    def print_result(self):
        content = self.get_data("content")

        if self.get_arg("pretty_print"):
            for c in content:
                print(f"{c.get("mode")} {c.get("type")} {c.get("hash")} {c.get("name")}")
        else:
            # TODO Show command manpage
            raise RuntimeError(f"Params required")