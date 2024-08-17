from collections import UserList
from re import match
from taipan_assistant.contacts.record.field import Field


class Phone(Field):
    # реалізація класу
    def __init__(self, value):
        if not match(r'^\d{10}$', value):
            raise ValueError('Phone number must be 10 digits')

        super().__init__(value=value)


class PhoneCollection(UserList):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return ' '.join(list(map(str, self.data)))
