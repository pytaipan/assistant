from colorama import Fore, Back, Style
from books.address_book import AddressBook, Record
from books.notebook import Notebook
from error_decorator import input_error
from output_formatter import format_success, format_error


@input_error
def contacts_handlers(command, books, *arguments):
    no_args_handlers_map = {
        'hello': hello_handler,
        'help': help_handler,
    }

    contact_handlers_map = {
        'add': add_contact_handler,
        'change': change_contact_handler,
        'phone': get_contact_handler,
        'all': get_all_contacts_handler,
        'add-birthday': add_birthday_handler,
        'show-birthday': get_birthday_handler,
        'birthdays': get_all_birthdays_handler,
    }

    notes_handlers_map = {
        'notes': get_all_notes_handler,
        'add-note': add_note_handler,
        'edit-note': edit_note_handler,
        'delete-note': delete_note_handler,
    }

    if command in no_args_handlers_map:
        return no_args_handlers_map[command]()

    if command in contact_handlers_map:
        return contact_handlers_map[command](books.address_book, *arguments)

    if command in notes_handlers_map:
        return notes_handlers_map[command](books.notebook, *arguments)

    raise KeyError(f'Command {command} was not found')


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
{Fore.LIGHTWHITE_EX}{Back.BLUE}notes{Style.RESET_ALL} - prints all notes
{Fore.LIGHTWHITE_EX}{Back.BLUE}add-note [text note]{Style.RESET_ALL} - adds a new note and prints it's ID
{Fore.LIGHTWHITE_EX}{Back.BLUE}edit-note [ID] [text note]{Style.RESET_ALL} - updates note with given ID
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
    return format_success('\n'.join(map(lambda name: f'{name}: {contacts[name].birthday}', contacts.keys())))


def get_all_notes_handler(notes: Notebook, *args):
    return format_success('\n'.join(map(lambda note: f'ID[{notes.index(note)}] Note: "{note}"', notes)))

def add_note_handler(notes: Notebook, *args):
    return format_success(f'Note add with ID: {notes.add_note(' '.join(args))}')


def edit_note_handler(notes: Notebook, id: str, *args):
    try:
        note = notes.get_note(int(id))
        note.edit(' '.join(args))
    except IndexError:
        return format_error('Note not found.')

    return format_success(f'Note #{id} updated')

def delete_note_handler(notes: Notebook, id: str, *args):
    try:
        notes.delete_note(int(id))
        return format_success(f'Note #{id} deleted')
    except IndexError:
        return format_error('Note not found.')
