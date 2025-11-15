"""
Address Book Bot - A command-line interface for managing contacts.

This module provides the main entry point for the address book bot,
which allows users to add, update, delete, and view contacts with
phone numbers and birthdays.
"""

import signal
import atexit
from colorama import Fore, Style
from core.commands import Command
from core.handlers import (
    add_contact, update_contact, get_all_contacts, search_contacts, get_one_contact,
    delete_contact, add_birthday, show_birthday, delete_birthday, show_upcoming_birthdays,
    add_note, list_notes, search_notes, search_notes_by_tags,
    edit_note, delete_note, add_email, delete_email, show_email, show_statistics, add_address, remove_address, show_address
)
from utils.parsers import parse_input, detect_command
from utils.help_formatter import (
    format_help_full,
    format_help_short,
    format_help_category,
    _header_line
)
from utils.input_enhancer import setup_readline
from storage.file_storage import load_data, save_data, load_notes, save_notes


# Global variables for data persistence
_book = None
_notebook = None


def save_all_data():
    """Save all data to persistent storage."""
    global _book, _notebook
    if _book is not None:
        try:
            save_data(_book)
        except (IOError, OSError, PermissionError):
            pass
    if _notebook is not None:
        try:
            save_notes(_notebook)
        except (IOError, OSError, PermissionError):
            pass


def get_goodbye_message():
    """Return goodbye message."""
    return (
        f"{_header_line()}\n"
        f"{Fore.GREEN}{Style.BRIGHT}👋 Goodbye!{Style.RESET_ALL} {Fore.CYAN}Thank you for using the assistant bot!{Style.RESET_ALL}\n"
        f"{_header_line()}"
    )


def print_interrupted_message():
    """Print interruption message and save data."""
    print(f"\n{_header_line()}")
    print(f"{Fore.YELLOW}{Style.BRIGHT}⚠️  Interrupted by user{Style.RESET_ALL}")
    print(f"{Fore.GREEN}{Style.BRIGHT}💾 Saving data...{Style.RESET_ALL}")
    save_all_data()
    print(f"{Fore.GREEN}✅ Data saved successfully!{Style.RESET_ALL}")
    print(f"{Fore.GREEN}{Style.BRIGHT}👋 Goodbye!{Style.RESET_ALL} {Fore.CYAN}Thank you for using the assistant bot!{Style.RESET_ALL}")
    print(f"{_header_line()}")


def signal_handler(signum, frame):  # pylint: disable=unused-argument
    """Signal handler for saving data before termination."""
    print(f"\n{_header_line()}")
    print(f"{Fore.YELLOW}{Style.BRIGHT}⚠️  Received signal {signum}, saving data...{Style.RESET_ALL}")
    save_all_data()
    print(f"{Fore.GREEN}✅ Data saved successfully!{Style.RESET_ALL}")
    print(f"{Fore.GREEN}{Style.BRIGHT}👋 Goodbye!{Style.RESET_ALL}")
    print(f"{_header_line()}")
    exit(0)


def get_output_by_command(command, args, book, notebook):
    """
    Process command and return result.

    Args:
        command: Command to execute
        args: Command arguments
        book: AddressBook instance
        notebook: NoteBook instance

    Returns:
        tuple: (command output, whether to exit the program)
    """
    is_break_main_loop = False
    command_output = None
    if command in (Command.EXIT_1, Command.EXIT_2):
        is_break_main_loop = True
        command_output = get_goodbye_message()
    elif command == Command.HELLO:
        command_output = "How can I help you?"
    elif command == Command.ADD_CONTACT:
        command_output = add_contact(args, book)
    elif command == Command.UPDATE_CONTACT:
        command_output = update_contact(args, book)
    elif command == Command.SHOW_ALL_CONTACTS:
        command_output = get_all_contacts(book)
    elif command == Command.SEARCH_CONTACTS:
        command_output = search_contacts(args, book)
    elif command == Command.SHOW_CONTACT:
        command_output = get_one_contact(args, book)
    elif command == Command.DELETE_CONTACT:
        command_output = delete_contact(args, book)
    elif command == Command.SET_BIRTHDAY:
        command_output = add_birthday(args, book)
    elif command == Command.SHOW_BIRTHDAY:
        command_output = show_birthday(args, book)
    elif command == Command.DELETE_BIRTHDAY:
        command_output = delete_birthday(args, book)
    elif command == Command.SHOW_UPCOMING_BIRTHDAYS:
        command_output = show_upcoming_birthdays(args, book)
    elif command == Command.SET_EMAIL:
        command_output = add_email(args, book)
    elif command == Command.DELETE_EMAIL:
        command_output = delete_email(args, book)
    elif command == Command.SHOW_EMAIL:
        command_output = show_email(args, book)
    elif command == Command.ADD_NOTE:
        command_output = add_note(args, notebook)
    elif command == Command.LIST_NOTES:
        command_output = list_notes(args, notebook)
    elif command == Command.SEARCH_NOTES:
        command_output = search_notes(args, notebook)
    elif command == Command.SEARCH_TAGS:
        command_output = search_notes_by_tags(args, notebook)
    elif command == Command.EDIT_NOTE:
        command_output = edit_note(args, notebook)
    elif command == Command.DELETE_NOTE:
        command_output = delete_note(args, notebook)
    elif command == Command.SET_ADDRESS:
        command_output = add_address(args, book)
    elif command == Command.DELETE_ADDRESS:
        command_output = remove_address(args, book)
    elif command == Command.SHOW_ADDRESS:
        command_output = show_address(args, book)
    elif command in Command.STATS:
        command_output = show_statistics(book, notebook)
    elif command in [Command.HELP, Command.HELP_ALT]:
        command_output = get_help_output(args)
    else:
        command_output = "Unknown command. Please try again."
    return command_output, is_break_main_loop


def _get_unknown_category_message(category):
    """Return message for unknown help category."""
    return (
        f"{_header_line()}\n"
        f"Unknown help category: {Fore.MAGENTA}'{category}'{Style.RESET_ALL}\n"
        f"Available categories: {Fore.BLUE}contacts{Style.RESET_ALL}, {Fore.BLUE}notes{Style.RESET_ALL}, {Fore.BLUE}birthdays{Style.RESET_ALL}, {Fore.BLUE}email{Style.RESET_ALL}\n"
        f"Use {Fore.CYAN}'{Command.HELP} short'{Style.RESET_ALL} for quick reference\n"
        f"Use {Fore.CYAN}'{Command.HELP}'{Style.RESET_ALL} for full help\n"
        f"{_header_line()}"
    )


def get_help_output(args):
    """
    Generates help output based on the provided arguments.

    Args:
        args (list): A list of strings representing the help categories or commands.

    Returns:
        str: A formatted string containing help information. If the first argument is recognized,
             it returns a short help, category-specific help, or an error message for unknown categories.
             If no arguments are provided, it returns the full help output.
    """
    try:
        if not args or len(args) == 0:
            return format_help_full()

        first_arg = args[0].lower()

        if first_arg in ["short", "s", "quick"]:
            return format_help_short()

        if first_arg in ["contacts", "notes", "birthdays", "email", "address"]:
            return format_help_category(first_arg)

        return _get_unknown_category_message(args[0])
    except Exception:
        return format_help_full()


def print_welcome_message():
    """Print welcome message."""
    print(f"{_header_line()}")
    print(f"{Fore.CYAN}{' ' * 20}{Style.BRIGHT}🤖 Welcome to the assistant bot!{Style.RESET_ALL}")
    print(f"{_header_line()}\n")


def setup_signal_handlers():
    """Setup signal handlers for graceful termination."""
    signal.signal(signal.SIGINT, signal_handler)   # Ctrl+C
    signal.signal(signal.SIGTERM, signal_handler)  # Terminal closure (Linux/Mac)
    if hasattr(signal, 'SIGHUP'):
        signal.signal(signal.SIGHUP, signal_handler)  # Terminal closure (Linux)


def run_main_loop(book, notebook):
    """Run main command processing loop."""
    try:
        while True:
            try:
                user_input = input(
                    f"{Fore.GREEN}{Style.BRIGHT}➜{Style.RESET_ALL} "
                    f"{Fore.LIGHTYELLOW_EX}Enter a command:{Style.RESET_ALL} "
                )
            except (KeyboardInterrupt, EOFError):
                # Ctrl+C or Ctrl+D - save data and exit
                print_interrupted_message()
                break

            try:
                command, *args = parse_input(user_input)
            except ValueError:
                # Handle unclosed quotes error from shlex.split()
                print(f"❌ Error: {Fore.RED}Unclosed quotes detected.{Style.RESET_ALL} Please check your input.")
                continue

            command, is_command_recognized = detect_command(command)
            if not is_command_recognized:
                continue

            output, is_exit = get_output_by_command(command, args, book, notebook)
            print(output)
            if is_exit:
                break
    except (KeyboardInterrupt, EOFError, Exception) as e:
        # Handle any unexpected errors during command execution
        if isinstance(e, (KeyboardInterrupt, EOFError)):
            print_interrupted_message()
        else:
            print(f"\n{Fore.RED}⚠️  Unexpected error occurred: {e}{Style.RESET_ALL}")
            print(f"{Fore.GREEN}💾 Saving data...{Style.RESET_ALL}")
    finally:
        # Always save data before exiting
        save_all_data()


if __name__ == "__main__":
    setup_readline(Command)
    _book = load_data()
    _notebook = load_notes()

    # Register save function for normal exit
    atexit.register(save_all_data)

    # Setup signal handlers
    setup_signal_handlers()

    # Print welcome message
    print_welcome_message()

    # Run main loop
    run_main_loop(_book, _notebook)
