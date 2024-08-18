from typing import Callable
from functools import wraps

from .output_formatter import format_error


def input_error(func: Callable):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError as e:
            return format_error(f'Invalid command. [KeyError {e}]')
        except ValueError as e:
            return format_error(f'Enter the argument for the command [ValueError {e}]')
        except IndexError as e:
            return format_error(f'Enter the argument for the command [IndexError {e}]')
        except TypeError as e:
            return format_error(f'Enter the argument for the command [TypeError {e}]')

    return wrapper
