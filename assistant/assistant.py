from assistant.address_book import AddressBook
from assistant.notebook import Notebook


class Assistant:
    def __init__(self):
        self.address_book = AddressBook()
        self.notebook = Notebook()
