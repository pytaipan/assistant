from ..command.command import Command
from ..command.command_registry import CommandRegistry
from ..contacts.address_book import AddressBook
from ..contacts.command_handler import CommandHandler as AddressBookCommandHandler
from ..notebook.notebook import Notebook


class Assistant(CommandRegistry):
    def __init__(self):
        super().__init__()

        self.address_book = AddressBook()
        self.notebook = Notebook()

        self.register(
            Command("contact", AddressBookCommandHandler(self.address_book), "Allows to manipulate contacts")
        )
