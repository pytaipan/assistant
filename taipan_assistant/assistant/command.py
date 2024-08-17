from typing import Callable


class Command:
    def __init__(self, name: str, handler: Callable, description: str = None):
        self.name = name
        self.__handler = handler
        self.description = description

    def __call__(self, *args, **kwargs):
        return self.__handler(*args, **kwargs)
