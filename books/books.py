from collections import UserDict

from books.address_book import AddressBook
from books.notebook import Notebook


class Books:
    def __init__(self):
        self.address_book = AddressBook()
        self.notebook = Notebook()
