from collections import UserDict

from .command import Command
from .output_formatter import format_error, format_success


class CommandRegistry(UserDict):
    def __init__(self):
        super().__init__()

    def register(self, command: Command):
        self.data[command.name] = command

    def commands(self) -> list[str]:
        return list(self.data.keys())

    def help(self, ns: str = '') -> str:
        res = ''

        for name, command in self.data.items():
            res += f'{command.help(name)}\n'.lstrip()

        return res

    def supports(self, command: str) -> bool:
        return command in self.data

    def _format_error(self, error):
        return format_error(error)

    def _format_success(self, message: str):
        return format_success(message)

    def _parse_bool_from_str(self, string: str) -> bool:
        return string.lower() == 'true'

    def __call__(self, *args, **kwargs):
        command = args[0]

        if command not in self.data:
            return "Command {} not found, try one of: {}".format(command, ", ".join(self.data.keys()))

        return self.data[command](*args[1:], **kwargs)

