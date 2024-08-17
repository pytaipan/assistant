from re import match

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
        return f'{{value: {super().__str__()}, primary:{self.primary} }}'
