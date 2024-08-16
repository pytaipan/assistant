from assistant.assistant import Assistant
from command_handler import hello_handler, help_handler, command_handlers
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
        assistant = load_data()
    except FileNotFoundError as e:
        assistant = Assistant()

    print(hello_handler())
    print(help_handler())
    try:
        while True:
            command, *arguments = parse_command(input('>>'))

            if command in ['exit', 'close']:
                print(format_success('Good bye!'))
                break

            print(command_handlers(command, assistant, *arguments))

    except KeyboardInterrupt:
        print(format_success('\nGood bye!'))
    finally:
        save_data(assistant)


if __name__ == '__main__':
    main()
