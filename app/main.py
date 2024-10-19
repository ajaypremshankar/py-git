import sys

from app.commands import command

def main():
    args = sys.argv[1:]

    command_obj = command.get_command(sys.argv[1], args)
    command_obj.execute()
    command_obj.print_result()


if __name__ == "__main__":
    main()
