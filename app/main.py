import sys

from app.commands import core

def main():
    command_obj = core.get_command(sys.argv[1], sys.argv[2:])
    command_obj.execute()
    command_obj.print_result()


if __name__ == "__main__":
    main()
