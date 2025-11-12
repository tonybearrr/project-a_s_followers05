"""
Utility functions for user confirmations.
"""

from colorama import Fore, Style


def confirm_action(message, default=False):
    """
    Ask user for confirmation.

    Args:
        message (str): Confirmation message
        default (bool): Default answer if user just presses Enter

    Returns:
        bool: True if confirmed, False otherwise
    """
    if default:
        default_text = f"{Fore.GREEN}[Y]{Style.RESET_ALL}/{Fore.RED}n{Style.RESET_ALL}"
    else:
        default_text = f"{Fore.GREEN}y{Style.RESET_ALL}/{Fore.RED}[N]{Style.RESET_ALL}"
    response = input(f"{Fore.YELLOW}-{Style.RESET_ALL} {message} ({default_text}): ").strip().lower()

    if not response:
        return default

    return response in ['y', 'yes', 'так', 'т']


def confirm_delete(entity_type, entity_name):
    """
    Confirm deletion of an entity.

    Args:
        entity_type (str): Type of entity (contact, note, etc.)
        entity_name (str): Name/identifier of entity

    Returns:
        bool: True if confirmed
    """
    message = (
        f"⚠️  {Fore.RED}Are you sure you want to delete {entity_type}"
        f"{Style.RESET_ALL} {Fore.CYAN}{entity_name}{Style.RESET_ALL}{Fore.RED}?{Style.RESET_ALL}"
    )
    return confirm_action(message, default=False)
