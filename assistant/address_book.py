from collections import UserDict
from record.record import Record
from search.engine import Engine


class AddressBook(UserDict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.search_engine = Engine(['name', 'phones'])

    def __setitem__(self, key, item):
        super().__setitem__(key, item)
        self.__add_record_to_index(item)

    def __delitem__(self, key):
        super().__delitem__(key)
        self.search_engine.remove_from_index(key)

    def add_record(self, record: Record):
        self.data[str(record.name)] = record
        self.__add_record_to_index(record)

    def find_by_name(self, name: str) -> Record:
        if name not in self.data.keys():
            raise ValueError('Record not found')

        return self.data[name]

    def search(self, search_term: str) -> list:
        return self.search_engine.find(search_term)

    def delete(self, name: str):
        if name not in self.data.keys():
            raise ValueError('Record not found')

        record = self.data.pop(name)
        self.search_engine.remove_from_index(record.name)

    def __add_record_to_index(self, record: Record):
        self.search_engine.add_to_index(record.name, record)
