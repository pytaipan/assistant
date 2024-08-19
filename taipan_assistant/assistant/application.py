import pickle

from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

from .assistant import Assistant
from .command_handler import command_handlers, hello_handler, help_handler
from .output_formatter import format_success


class Application:
    def __init__(self):
        pass

    def __load_data(self, filename="storage.bin"):
        with open(filename, "rb") as f:
            return pickle.load(f)

    def __save_data(self, data_dict, filename="storage.bin"):
        with open(filename, "wb") as f:
            pickle.dump(data_dict, f)

    def __parse_command(self, input_sting: str):
        if input_sting == "":
            return "help",

        args = []
        arg = ""
        open_char = None

        for char in input_sting:
            if arg == "":
                if char in ["'", '"', ' '] and open_char is None:
                    open_char = char
                    continue

                if open_char is None:
                    open_char = " "

                arg += char
                continue

            if char == open_char:
                args.append(arg)
                open_char = None
                arg = ""
                continue

            arg += char

        if arg != "":
            args.append(arg)

        command, *arguments = args

        return command, *arguments

    def run(self):
        try:
            assistant = self.__load_data()
        except FileNotFoundError:
            assistant = Assistant()

        print(hello_handler())
        print(help_handler())

        # Предполагаемый список доступных команд
        commands = ['help', 'hello', 'add', 'change', 'phone', 'all', 'delete-contact', 'add-birthday', 'show-birsthday',
                    'birthdays', 'notes', 'add-note', 'edit-note', 'delete-note', 'search-note', 'add-note-tag', 'notes-by-tags',
                    'close', 'exit', 'search-contacts', 'upcoming-birthdays']


        # Создание объекта WordCompleter с доступными командами
        command_completer = WordCompleter(commands, ignore_case=True)

        try:
            while True:
                user_input = prompt('>> ', completer=command_completer)
                command, *arguments = self.__parse_command(user_input)

                if command in ['exit', 'close']:
                    print(format_success('Good bye!'))
                    break

                print(command_handlers(command, assistant, *arguments))

        except KeyboardInterrupt:
            print(format_success('\nGood bye!'))
        finally:
            self.__save_data(assistant)
