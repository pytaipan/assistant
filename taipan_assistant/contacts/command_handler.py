from colorama import Fore, Back, Style
from .address_book import AddressBook
from .record.record import Record
from ..command.command import Command
from ..command.command_registry import CommandRegistry
from ..command.error_decorator import input_error


class CommandHandler(CommandRegistry):
    def __init__(self, address_book: AddressBook):
        super().__init__()

        self.__address_book = address_book

        self.register(Command(
            'add',
            self.add_command,
            f'{Fore.LIGHTWHITE_EX}{Back.BLUE}add [name] [phone number]{Style.RESET_ALL} - create a contact with a phone number',
        ))
        self.register(Command(
            'delete-contact',
            self.delete_contact_command,
            f'{Fore.LIGHTWHITE_EX}{Back.BLUE}delete-contact [name] {Style.RESET_ALL} - delete contact'
        ))
        self.register(Command(
            'add-email',
            self.add_email_command,
            f'{Fore.LIGHTWHITE_EX}{Back.BLUE}add-email [name] [email] [is_primary]{Style.RESET_ALL} - Add or change email in contact, or create new contact with email if not exists'
        ))
        self.register(Command(
            'change-email',
            self.change_email_command,
            f'{Fore.LIGHTWHITE_EX}{Back.BLUE}change-email [name] [old_email_value] [new_email_value] [is_primary]{Style.RESET_ALL} - Add or change email in contact, or create new contact with email if not exists'
        ))
        self.register(Command(
            'set-address',
            self.set_address_command,
            f'{Fore.LIGHTWHITE_EX}{Back.BLUE}set-address [name] [address]{Style.RESET_ALL} - set address into contact'
        ))
        self.register(Command(
            'change',
            self.change_command,
            f'{Fore.LIGHTWHITE_EX}{Back.BLUE}change [name] [phone number]{Style.RESET_ALL} - changes a contact phone number '
        ))
        self.register(Command(
            'phone',
            self.phone_command,
            f'{Fore.LIGHTWHITE_EX}{Back.BLUE}phone [name]{Style.RESET_ALL} - prints contacts phone number'
        ))
        self.register(Command(
            'all',
            self.all_command,
            f'{Fore.LIGHTWHITE_EX}{Back.BLUE}all{Style.RESET_ALL} - prints all contacts'
        ))
        self.register(Command(
            'add-birthday',
            self.add_birthday_command,
            f'{Fore.LIGHTWHITE_EX}{Back.BLUE}add-birthday [name] [birthday]{Style.RESET_ALL} - adds birthday to a contact'
        ))
        self.register(Command(
            'show-birthday',
            self.show_birthday_command,
            f"{Fore.LIGHTWHITE_EX}{Back.BLUE}show-birthday [name]{Style.RESET_ALL} - prints contact's birthday"
        ))
        self.register(Command(
            'birthdays',
            self.birthdays_command,
            f'{Fore.LIGHTWHITE_EX}{Back.BLUE}birthdays{Style.RESET_ALL} - prints all birthdays'
        ))
        self.register(Command(
            'upcoming-birthdays',
            self.upcoming_birthdays_command,
            f'{Fore.LIGHTWHITE_EX}{Back.BLUE}upcoming-birthdays [number of days from today]{Style.RESET_ALL} - search for contacts on their birthday within a specified number of days from today'
        ))
        self.register(Command(
            'search',
            self.search_command,
            f'{Fore.LIGHTWHITE_EX}{Back.BLUE}search-contacts [search_term]{Style.RESET_ALL} - search contacts by names or phones'
        ))

    @input_error
    def add_command(self, name: str, phone: str):
        name = name.lower().capitalize()

        try:
            record = self.__address_book.find_by_name(name)
        except ValueError:
            record = Record(name)

        record.add_phone(phone)
        self.__address_book[name] = record

        return self._format_success('Contact added')

    @input_error
    def add_email_command(self, name: str, email: str, is_primary: str = "False"):
        name = name.lower().capitalize()
        primary = self._parse_bool_from_str(is_primary)

        record = self.__address_book.find_by_name(name)
        if record is None:
            record = Record(name)

        record.add_email(email, primary)
        self.__address_book[name] = record

        return self._format_success('Email added')

    @input_error
    def change_email_command(self, name: str, old_email: str, new_email: str, is_primary: str):
        name = name.lower().capitalize()
        primary = self._parse_bool_from_str(is_primary)

        try:
            record = self.__address_book.find_by_name(name)
            record.change_email(old_email, new_email, primary)
            self.__address_book[name] = record

            return self._format_success('Email updated.')
        except ValueError as error:
            return self._format_error(error)

    @input_error
    def set_address_command(self, name: str, *args):
        try:
            record = self.__address_book.find_by_name(name)
            record.set_address(' '.join(args))

            return self._format_success('The address is set.')
        except ValueError as error:
            return self._format_error(error)

    @input_error
    def change_command(self, name: str, phone: str):
        name = name.lower().capitalize()
        try:
            record = self.__address_book.find_by_name(name)
            record.edit_phone(record.phones[0], phone)
            self.__address_book[name] = record

            return self._format_success('Contact updated.')
        except ValueError:
            return self._format_error('Contact not found.')

    @input_error
    def phone_command(self, name: str):
        try:
            return self.__address_book.find_by_name(name.lower().capitalize())
        except ValueError:
            return self._format_error('Contact not found.')

    @input_error
    def all_command(self):
        if len(self.__address_book) == 0:
            return self._format_error('AddressBook is empty.')
        return self.__records_to_str(self.__address_book.values())

    @input_error
    def add_birthday_command(self, name: str, birthday: str):
        try:
            self.__address_book.find_by_name(name.lower().capitalize()).add_birthday(birthday)
            return self._format_success('Contact updated. Birthday added.')
        except ValueError as error:
            return self._format_error(error)

    @input_error
    def show_birthday_command(self, name: str, *args):
        try:
            return self.__address_book.find_by_name(name.lower().capitalize()).birthday
        except ValueError:
            return self._format_error('Contact not found.')

    @input_error
    def birthdays_command(self, *args):
        return self._format_success('\n'.join(map(lambda name: f'{name}: {self.__address_book[name].birthday}', self.__address_book.keys())))

    @input_error
    def upcoming_birthdays_command(self, coming_days: str):
        records = self.__address_book.get_upcoming_birthdays(int(coming_days))
        if len(records) == 0:
            return self._format_error('Contacts not found.')
        return self.__records_to_str(records)


    @input_error
    def search_command(self, search: str):
        records = self.__address_book.search(search)
        if len(records) == 0:
            return self._format_error('Contacts not found.')
        return self.__records_to_str(records)

    @input_error
    def delete_contact_command(self, name: str):
        try:
            self.__address_book.delete(name)
            return self._format_success('Contact deleted.')
        except ValueError as error:
            return self._format_error(error)

    def __records_to_str(self, records: iter):
        return '\n'.join(map(lambda record: f'{record.name}: {record}', records))
