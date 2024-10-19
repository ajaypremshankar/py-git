import sys

from app.commands import impl

def main():
    command_obj = command.get_command(sys.argv[1], sys.argv[1:])
    command_obj.execute()
    command_obj.print_result()


if __name__ == "__main__":
    main()
