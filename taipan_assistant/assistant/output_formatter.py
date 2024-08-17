from colorama import Fore, Back, Style


def format_error(error: str):
    return f'{Fore.LIGHTWHITE_EX}{Back.RED}{error}{Style.RESET_ALL}'


def format_success(message: str):
    return f'{Fore.GREEN}{message}{Style.RESET_ALL}'
