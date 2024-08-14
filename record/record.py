from record.birthday import Birthday
from record.name import Name
from record.phone import Phone


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
