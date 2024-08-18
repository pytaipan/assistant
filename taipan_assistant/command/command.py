from typing import Callable


class Command:
    def __init__(self, name: str, handler: Callable, description: str = None):
        self.name = name
        self.__handler = handler
        self.description = description

    def __call__(self, *args, **kwargs):
        return self.__handler(*args, **kwargs)

    def supports(self, command: str) -> bool:
        return command == self.name

    def help(self, ns: str) -> str:
        return f"{ns} {self.name} - {self.description}"
