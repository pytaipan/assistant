from colorama import Fore, Back, Style
from address_book import AddressBook, Record
from error_decorator import input_error
from output_formatter import format_success, format_error


@input_error
def contacts_handlers(command, contacts, *arguments):
    no_args_handlers_map = {
        'hello': hello_handler,
        'help': help_handler,
    }

    handlers_map = {
        'add': add_contact_handler,
        'change': change_contact_handler,
        'phone': get_contact_handler,
        'all': get_all_contacts_handler,
        'add-birthday': add_birthday_handler,
        'show-birthday': get_birthday_handler,
        'birthdays': get_all_birthdays_handler,
    }

    if command in no_args_handlers_map:
        return no_args_handlers_map[command]()

    return handlers_map[command](contacts, *arguments)


def hello_handler():
    return 'Hello, how can I help you?'


def help_handler():
    return f'''Possible commands:
{Fore.LIGHTWHITE_EX}{Back.BLUE}help{Style.RESET_ALL} - prints list of available commands
{Fore.LIGHTWHITE_EX}{Back.BLUE}hello{Style.RESET_ALL} - prints a greeting 
{Fore.LIGHTWHITE_EX}{Back.BLUE}add [name] [phone number]{Style.RESET_ALL} - create a contact with a phone number
{Fore.LIGHTWHITE_EX}{Back.BLUE}change [name] [phone number]{Style.RESET_ALL} - changes a contact phone number 
{Fore.LIGHTWHITE_EX}{Back.BLUE}phone [name]{Style.RESET_ALL} - prints contacts phone number
{Fore.LIGHTWHITE_EX}{Back.BLUE}all{Style.RESET_ALL} - prints all contacts
{Fore.LIGHTWHITE_EX}{Back.BLUE}add-birthday [name] [birthday]{Style.RESET_ALL} - adds birthday to a contact
{Fore.LIGHTWHITE_EX}{Back.BLUE}show-birthday [name]{Style.RESET_ALL} - prints contact's birthday
{Fore.LIGHTWHITE_EX}{Back.BLUE}birthdays{Style.RESET_ALL} - prints all birthdays
{Fore.LIGHTWHITE_EX}{Back.BLUE}close{Style.RESET_ALL} або {Fore.YELLOW}{Back.BLUE}exit{Style.RESET_ALL} - terminates a program
    '''


@input_error
def add_contact_handler(contacts: AddressBook, name: str, phone: str):
    name = name.lower().capitalize()
    record = Record(name)
    record.add_phone(phone)
    contacts[name] = record
    return format_success('Contact added')


@input_error
def change_contact_handler(contacts: AddressBook, name: str, phone: str):
    name = name.lower().capitalize()
    try:
        record = contacts.find(name)
        record.edit_phone(record.phones[0], phone)

        return format_success('Contact updated.')
    except ValueError:
        return format_error('Contact not found.')


@input_error
def get_contact_handler(contacts: AddressBook, name: str, *args):
    try:
        return contacts.find(name.lower().capitalize())
    except ValueError:
        return format_error('Contact not found.')


def get_all_contacts_handler(contacts: AddressBook, *args):
    if len(contacts) == 0:
        return format_error('AddressBook is empty.')
    return '\n'.join(map(lambda name: f'{name}: {contacts[name]}', contacts.keys()))


def add_birthday_handler(contacts: AddressBook, name: str, birthday: str):
    try:
        contacts.find(name.lower().capitalize()).add_birthday(birthday)
        return format_success('Contact updated.')
    except ValueError:
        return format_error('Contact not found.')


def get_birthday_handler(contacts: AddressBook, name: str, *args):
    try:
        return contacts.find(name.lower().capitalize()).birthday
    except ValueError:
        return format_error('Contact not found.')


def get_all_birthdays_handler(contacts: AddressBook, *args):
    return '\n'.join(map(lambda name: f'{name}: {contacts[name].birthday}', contacts.keys()))







