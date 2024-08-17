from ..contacts.address_book import AddressBook
from ..notebook.notebook import Notebook


class Assistant:
    def __init__(self):
        self.address_book = AddressBook()
        self.notebook = Notebook()
