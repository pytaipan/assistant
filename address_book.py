from collections import UserDict
from re import match
from datetime import datetime


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    # реалізація класу
    pass


class Phone(Field):
    # реалізація класу
    def __init__(self, value):
        if not match(r'^\d{10}$', value):
            raise ValueError('Phone number must be 10 digits')

        super().__init__(value=value)


class Birthday(Field):
    def __init__(self, value):
        try:
            super().__init__(value=datetime.strptime(value, '%d.%m.%Y'))
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

    def __str__(self):
        return self.value.strftime("%d.%m.%Y")


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone: str):
        self.phones.append(Phone(phone))

    def add_birthday(self, birthday: str):
        self.birthday = Birthday(birthday)

    def remove_phone(self, phone: str):
        phone_field = Phone(phone)
        if phone_field not in self.phones:
            raise ValueError(f'Phone number {phone} does not belong record {self.name}')

        self.phones.remove(phone_field)

    def edit_phone(self, old_phone: str, new_phone: str):
        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = new_phone
                break

    def find_phone(self, phone: str) -> Phone:
        for phone_field in self.phones:
            if phone_field.value == phone:
                return phone_field

        raise ValueError(f'Phone number {phone} does not belong record {self.name}')

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[str(record.name)] = record

    def find(self, name: str) -> Record:
        if name not in self.data.keys():
            raise ValueError('Record not found')

        return self.data[name]

    def delete(self, name: str):
        if name not in self.data.keys():
            raise ValueError('Record not found')

        self.data.pop(name)
