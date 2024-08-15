from books.books import Books
from command_handler import hello_handler, help_handler, contacts_handlers
from error_decorator import input_error
from file_storage import load_data, save_data
from output_formatter import format_success


@input_error
def parse_command(input_sting: str):
    command, *arguments = input_sting.split()
    if command not in ['add-note', 'edit-note'] and len(arguments) > 2:
        last_arg = arguments.pop()
        return [command, ' '.join(arguments), last_arg]

    return command, *arguments


def main():
    try:
        books = load_data()
    except FileNotFoundError as e:
        books = Books()

    print(hello_handler())
    print(help_handler())
    try:
        while True:
            command, *arguments = parse_command(input('>>'))

            if command in ['exit', 'close']:
                print(format_success('Good bye!'))
                break

            print(contacts_handlers(command, books, *arguments))

    except KeyboardInterrupt:
        print(format_success('\nGood bye!'))
    finally:
        save_data(books)


if __name__ == '__main__':
    main()
