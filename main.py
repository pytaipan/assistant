from address_book import AddressBook
from command_handler import hello_handler, help_handler, contacts_handlers
from error_decorator import input_error
from file_storage import load_data, save_data
from output_formatter import format_success
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter


@input_error
def parse_command(input_sting: str):
    command, *arguments = input_sting.split()
    if len(arguments) > 2:
        last_arg = arguments.pop()
        return [command, ' '.join(arguments), last_arg]

    return command, *arguments


def main():
    try:
        contacts = load_data()
    except FileNotFoundError:
        contacts = AddressBook()

    print(hello_handler())
    print(help_handler())

    # Предполагаемый список доступных команд
    commands = [ 'help', 'hello', 'add', 'change', 'phone', 'all', 'add-birthday', 'show-birsthday', 'birthdays','close','exit']

    # Создание объекта WordCompleter с доступными командами
    command_completer = WordCompleter(commands, ignore_case=True)

    try:
        while True:            
            user_input = prompt('>> ', completer=command_completer)
            command, *arguments = parse_command(user_input)

            if command in ['exit', 'close']:
                print(format_success('Good bye!'))
                break

            print(contacts_handlers(command, contacts, *arguments))

    except KeyboardInterrupt:
        print(format_success('\nGood bye!'))
    finally:
        save_data(contacts)

if __name__ == '__main__':
    main()
