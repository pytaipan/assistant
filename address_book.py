from collections import UserDict
from record.record import Record


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
