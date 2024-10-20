import sys

from app.commands.core import get_command

def main():
    command_name = sys.argv[1]
    command_line_args = sys.argv[2:]
    command_obj = get_command(command_name, command_line_args )
    command_obj.execute()
    command_obj.print_result()


if __name__ == "__main__":
    main()
