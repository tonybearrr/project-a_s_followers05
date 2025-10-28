"""
Decorators for the address book bot.

This module contains decorators that handle common errors and provide
consistent error messages across all handler functions.
"""

from functools import wraps


def input_error(func):
    """
    Decorator to handle common input errors and provide user-friendly messages.

    Handles the following exceptions:
    - ValueError: Returns "Enter the argument for the command"
    - KeyError: Returns "Contact not found"
    - IndexError: Returns "Enter the argument for the command"
    - AttributeError: Returns "Contact not found"
    Args:
        func: Function to be decorated

    Returns:
        function: Decorated function with error handling
    """
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Enter the argument for the command"
        except KeyError:
            return "Contact not found"
        except IndexError:
            return "Enter the argument for the command"
        except AttributeError:
            return "Contact not found"
    return inner
