from collections import UserDict

from .command import Command


class CommandRegistry(UserDict):
    def __init__(self):
        super().__init__()

    def register(self, command: Command):
        self.data[command.name] = command

    def list(self) -> list[str]:
        return list(self.data.keys())

