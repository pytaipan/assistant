from re import match
from colorama import Fore, Back, Style

from taipan_assistant.contacts.record.field import Field


class Email(Field):

    def __init__(self, value: str, primary: bool):
        if not match(r'^.+@.+\..+$', value):
            raise ValueError(
                'Email should be in format {one or more any char}@{one or more any char}.{one or more any char}'
            )

        self.primary = primary
        super().__init__(value=value)

    def __str__(self):
        if self.primary:
            return f'{Fore.LIGHTWHITE_EX}{Back.GREEN}{super().__str__()}{Style.RESET_ALL}'

        return f'{super().__str__()}'
