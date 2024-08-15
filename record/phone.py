from re import match

from record.field import Field


class Phone(Field):
    # реалізація класу
    def __init__(self, value):
        if not match(r'^\d{10}$', value):
            raise ValueError('Phone number must be 10 digits')

        super().__init__(value=value)
