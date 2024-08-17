from datetime import datetime
from taipan_assistant.contacts.record.field import Field


class Birthday(Field):
    def __init__(self, value):
        try:
            super().__init__(value=datetime.strptime(value, '%d.%m.%Y'))
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

    def __str__(self):
        return self.value.strftime("%d.%m.%Y")
