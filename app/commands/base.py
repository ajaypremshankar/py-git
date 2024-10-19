from abc import ABC, abstractmethod

class CommandOutput:
    def __init__(self, status: bool,
                 message: str = "",
                 data: dict = None):
        self.status = status
        self.data = data
        self.message = message
        self.output = None

class Command(ABC):
    """
    Abstract base class for Command objects.
    Concrete commands must implement the 'execute' method.
    """

    def __init__(self, args):
        self.args = args
        self.output = None

    @abstractmethod
    def execute(self):
        """
        Execute the command.
        """
        pass

    @abstractmethod
    def print_result(self):
        """
        Execute the command.
        """
        pass

    def get_data(self, key: str):
        return self.output.data.get(key, None)

    def execution_result(self):
        return self.output

    def is_success(self):
        return self.output.status

    def get_arg(self, key: str, default_val = None):
        return self.args.get(key, default_val)
