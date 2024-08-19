from colorama import Fore, Back, Style
from taipan_assistant.assistant.error_decorator import input_error
from taipan_assistant.assistant.output_formatter import format_success, format_error
from taipan_assistant.contacts.address_book import AddressBook
from taipan_assistant.contacts.record.record import Record
from taipan_assistant.notebook.notebook import Notebook


@input_error
def command_handlers(command, assistant, *arguments):
    no_args_handlers_map = {
        'hello': hello_handler,
        'help': help_handler,
    }

    contact_handlers_map = {
        'add': add_contact_handler,
        'add-email': add_email_handler,
        'change-email': change_email_handler,
        'set-address': set_address,
        'change': change_phone_handler,
        'phone': get_contact_handler,
        'all': get_all_contacts_handler,
        'add-birthday': add_birthday_handler,
        'show-birthday': get_birthday_handler,
        'birthdays': get_all_birthdays_handler,
        'upcoming-birthdays': get_upcoming_birthdays,
        'search-contacts': search_contacts,
        'delete-contact': delete_contact,
    }

    notes_handlers_map = {
        'notes': get_all_notes_handler,
        'add-note': add_note_handler,
        'edit-note': edit_note_handler,
        'delete-note': delete_note_handler,
        'search-note': search_note_handler,
        'add-note-tag': add_tag_to_note_handler,
        'notes-by-tags': sort_notes_by_tags,
    }

    if command in no_args_handlers_map:
        return no_args_handlers_map[command]()

    if command in contact_handlers_map:
        return contact_handlers_map[command](assistant.address_book, *arguments)

    if command in notes_handlers_map:
        return notes_handlers_map[command](assistant.notebook, *arguments)

    raise KeyError(f'Command {command} was not found')


def hello_handler():
    return 'Hello, how can I help you?'


def help_handler():
    return f'''Possible commands:
{Fore.LIGHTWHITE_EX}{Back.BLUE}help{Style.RESET_ALL} - prints list of available commands
{Fore.LIGHTWHITE_EX}{Back.BLUE}hello{Style.RESET_ALL} - prints a greeting 
{Fore.LIGHTWHITE_EX}{Back.BLUE}add [name] [phone number]{Style.RESET_ALL} - create a contact with a phone number
{Fore.LIGHTWHITE_EX}{Back.BLUE}add-email [name] [email] [is_primary]{Style.RESET_ALL} - Add or change email in contact, or create new contact with email if not exists
{Fore.LIGHTWHITE_EX}{Back.BLUE}change-email [name] [old_email_value] [new_email_value] [is_primary]{Style.RESET_ALL} - Add or change email in contact, or create new contact with email if not exists
{Fore.LIGHTWHITE_EX}{Back.BLUE}set-address [name] [address]{Style.RESET_ALL} - set address into contact
{Fore.LIGHTWHITE_EX}{Back.BLUE}change [name] [phone number]{Style.RESET_ALL} - changes a contact phone number 
{Fore.LIGHTWHITE_EX}{Back.BLUE}delete-contact [name] {Style.RESET_ALL} - delete contact
{Fore.LIGHTWHITE_EX}{Back.BLUE}phone [name]{Style.RESET_ALL} - prints contacts phone number
{Fore.LIGHTWHITE_EX}{Back.BLUE}all{Style.RESET_ALL} - prints all contacts
{Fore.LIGHTWHITE_EX}{Back.BLUE}search-contacts [search_term]{Style.RESET_ALL} - search contacts by names or phones
{Fore.LIGHTWHITE_EX}{Back.BLUE}add-birthday [name] [birthday]{Style.RESET_ALL} - adds birthday to a contact
{Fore.LIGHTWHITE_EX}{Back.BLUE}show-birthday [name]{Style.RESET_ALL} - prints contact's birthday
{Fore.LIGHTWHITE_EX}{Back.BLUE}birthdays{Style.RESET_ALL} - prints all birthdays
{Fore.LIGHTWHITE_EX}{Back.BLUE}upcoming-birthdays [number of days from today]{Style.RESET_ALL} - search for contacts on their birthday within a specified number of days from today
{Fore.LIGHTWHITE_EX}{Back.BLUE}notes{Style.RESET_ALL} - prints all notes
{Fore.LIGHTWHITE_EX}{Back.BLUE}notes-by-tags{Style.RESET_ALL} - prints all notes sorted by tags
{Fore.LIGHTWHITE_EX}{Back.BLUE}add-note [title] [text note]{Style.RESET_ALL} - adds a new note and prints it's ID
{Fore.LIGHTWHITE_EX}{Back.BLUE}edit-note [ID] [text note]{Style.RESET_ALL} - updates note with given ID
{Fore.LIGHTWHITE_EX}{Back.BLUE}delete-note [ID]{Style.RESET_ALL} - removes note with given ID
{Fore.LIGHTWHITE_EX}{Back.BLUE}search-note [text]{Style.RESET_ALL} - searches for notes by search phrase
{Fore.LIGHTWHITE_EX}{Back.BLUE}add-note-tag [ID] [tag]{Style.RESET_ALL} - adds a tag to a note
{Fore.LIGHTWHITE_EX}{Back.BLUE}close{Style.RESET_ALL} або {Fore.YELLOW}{Back.BLUE}exit{Style.RESET_ALL} - terminates a program
    '''


@input_error
def add_contact_handler(contacts: AddressBook, name: str, phone: str):
    name = name.lower().capitalize()

    try:
        record = contacts.find_by_name(name)
    except ValueError:
        record = Record(name)

    record.add_phone(phone)
    contacts[name] = record

    return format_success('Contact added')


@input_error
def add_email_handler(contacts: AddressBook, name: str, email: str, is_primary: str = "False"):
    name = name.lower().capitalize()
    primary = parser_bool_from_str(is_primary)

    record = contacts.find_by_name(name)
    if record is None:
        record = Record(name)

    record.add_email(email, primary)
    contacts[name] = record

    return format_success('Email added')


@input_error
def change_phone_handler(contacts: AddressBook, name: str, phone: str):
    name = name.lower().capitalize()
    try:
        record = contacts.find_by_name(name)
        record.edit_phone(record.phones[0], phone)
        contacts[name] = record

        return format_success('Contact updated.')
    except ValueError:
        return format_error('Contact not found.')


@input_error
def change_email_handler(contacts: AddressBook, name: str, old_email: str, new_email: str, is_primary: str):
    name = name.lower().capitalize()
    primary = parser_bool_from_str(is_primary)

    try:
        record = contacts.find_by_name(name)
        record.change_email(old_email, new_email, primary)
        contacts[name] = record

        return format_success('Email updated.')
    except ValueError as error:
        return format_error(error)


@input_error
def set_address(contacts: AddressBook, name: str, *args):
    try:
        record = contacts.find_by_name(name)
        record.set_address(' '.join(args))

        return format_success('The address is set.')
    except ValueError as error:
        return format_error(error)


@input_error
def get_contact_handler(contacts: AddressBook, name: str, *args):
    try:
        return contacts.find_by_name(name.lower().capitalize())
    except ValueError:
        return format_error('Contact not found.')


def get_all_contacts_handler(contacts: AddressBook, *args):
    if len(contacts) == 0:
        return format_error('AddressBook is empty.')
    return __records_to_str(contacts.values())


def add_birthday_handler(contacts: AddressBook, name: str, birthday: str):
    try:
        contacts.find_by_name(name.lower().capitalize()).add_birthday(birthday)
        return format_success('Contact updated.')
    except ValueError as error:
        return format_error(error)


def search_contacts(contacts: AddressBook, search_term: str) -> str:
    records = contacts.search(search_term)
    if len(records) == 0:
        return format_error('Contacts not found.')
    return __records_to_str(records)


def delete_contact(contacts: AddressBook, name: str) -> str:
    try:
        contacts.delete(name)
        return format_success('Contact deleted.')
    except ValueError as error:
        return format_error(error)


def get_birthday_handler(contacts: AddressBook, name: str, *args):
    try:
        return contacts.find_by_name(name.lower().capitalize()).birthday
    except ValueError:
        return format_error('Contact not found.')


def get_upcoming_birthdays(contacts: AddressBook, coming_days: str):
    records = contacts.get_upcoming_birthdays(int(coming_days))
    if len(records) == 0:
        return format_error('Contacts not found.')
    return __records_to_str(records)


def get_all_birthdays_handler(contacts: AddressBook, *args):
    return format_success('\n'.join(map(lambda name: f'{name}: {contacts[name].birthday}', contacts.keys())))


def get_all_notes_handler(notes: Notebook, *args):
    return format_success('\n\n\n'.join(map(lambda note_id: f'Note[{note_id}]\n{notes[note_id]}', notes.keys())))


def add_note_handler(notes: Notebook, title: str, text: str, *args):
    return format_success(f'Note added with ID: {notes.add_note(title, text)}')


def edit_note_handler(notes: Notebook, note_id: str, text: str, *args):
    try:
        notes.edit_note(note_id, text)
    except IndexError:
        return format_error('Note not found.')

    return format_success(f'Note #{note_id} updated')


def delete_note_handler(notes: Notebook, note_id: str, *args):
    try:
        notes.delete_note(note_id)
        return format_success(f'Note #{note_id} deleted')
    except IndexError:
        return format_error('Note not found.')


def search_note_handler(notes: Notebook, phrase: str, *args):
    notes = notes.find_notes(phrase)
    return format_success('\n'.join(map(lambda note: f'Note: "{note}"', notes)))


def add_tag_to_note_handler(notes: Notebook, note_id: str, tag: str, *args):
    try:
        notes.add_tag(note_id, tag)
        return format_success(f'Note #{note_id} updated')
    except IndexError:
        return format_error('Note not found.')


def sort_notes_by_tags(notes: Notebook, *args):
    return_text = ''
    for tag, notes in notes.sort_notes_by_tags().items():
        return_text += format_success(f'Tag: "{tag}", Notes:\n')
        for note_id, note in notes.items():
            return_text += format_success(f'Note[{note_id}]\n{note}')
        return_text += format_success(f'\n{'='*10}\n')

    return return_text


def format_notes_dict(notes):
    return format_success('\n'.join(map(lambda note_id: f'ID[{note_id}] Note: "{notes[note_id]}"', notes.keys())))


def parser_bool_from_str(val: str) -> bool:
    return val.lower() == 'true'


def __records_to_str(records: iter) -> str:
    return '\n'.join(map(lambda record: f'{record}', records))
