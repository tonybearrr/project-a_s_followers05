"""
Address Book Bot - A command-line interface for managing contacts.

This module provides the main entry point for the address book bot,
which allows users to add, update, delete, and view contacts with
phone numbers and birthdays.
"""

from core.commands import Command
from core.handlers import (
    add_contact, update_contact, get_all_contacts, search_contacts, get_one_contact,
    delete_contact, add_birthday, show_birthday, show_upcoming_birthdays,
    add_note, list_notes, search_notes, search_notes_by_tags,
    edit_note, delete_note, add_email, delete_email, show_email
)
from utils.parsers import parse_input
from utils.help_formatter import (
    format_help_full,
    format_help_short,
    format_help_category
)
from storage.file_storage import load_data, save_data, load_notes, save_notes
from colorama import Fore, Style


def get_output_by_command(command, args, book, notebook):
    """
    Main function that runs the address book bot.

    Creates an AddressBook and NoteBook instances and runs the main command loop,
    processing user commands until 'close' or 'exit' is entered.
    """
    is_break_main_loop = False
    command_output = None
    if command in (Command.EXIT_1, Command.EXIT_2):
        is_break_main_loop = True
        command_output = (
            f"{Fore.CYAN}{'═'*70}{Style.RESET_ALL}\n"
            f"{Fore.GREEN}{Style.BRIGHT}👋 Goodbye!{Style.RESET_ALL} {Fore.CYAN}Thank you for using the assistant bot!{Style.RESET_ALL}\n"
            f"{Fore.CYAN}{'═'*70}{Style.RESET_ALL}"
        )
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
    elif command == Command.ADD_BIRTHDAY:
        command_output = add_birthday(args, book)
    elif command == Command.SHOW_BIRTHDAY:
        command_output = show_birthday(args, book)
    elif command == Command.SHOW_UPCOMING_BIRTHDAYS:
        command_output = show_upcoming_birthdays(args, book)
    elif command == Command.ADD_EMAIL:
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
    elif command in [Command.HELP, Command.HELP_ALT]:
        try:
            if args and len(args) > 0:
                first_arg = args[0].lower()

            # Короткий help
                if first_arg in ["short", "s", "quick"]:
                    command_output = format_help_short()
                # Help по категорії
                elif first_arg in ["contacts", "notes", "birthdays", "email"]:
                    command_output = format_help_category(first_arg)
                else:
                    # Невідома категорія
                    command_output = (
                        f"{Fore.CYAN}{'═'*70}{Style.RESET_ALL}\n"
                        f"Unknown help category: {Fore.MAGENTA}'{args[0]}'{Style.RESET_ALL}\n"
                        f"Available categories: {Fore.BLUE}contacts{Style.RESET_ALL}, {Fore.BLUE}notes{Style.RESET_ALL}, {Fore.BLUE}birthdays{Style.RESET_ALL}, {Fore.BLUE}email{Style.RESET_ALL}\n"
                        f"Use {Fore.CYAN}'{Command.HELP} short'{Style.RESET_ALL} for quick reference\n"
                        f"Use {Fore.CYAN}'{Command.HELP}'{Style.RESET_ALL} for full help\n"
                        f"{Fore.CYAN}{'═'*70}{Style.RESET_ALL}"
                    )
            else:
                # Повний help (без аргументів)
                command_output = format_help_full()
        except Exception:
            command_output = format_help_full()
    else:
        command_output = "Unknown command. Please try again."
    return command_output, is_break_main_loop


if __name__ == "__main__":
    book = load_data()
    notebook = load_notes()
    print(f"{Fore.CYAN}{'═'*70}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{' '*20}{Style.BRIGHT}🤖 Welcome to the assistant bot!{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'═'*70}{Style.RESET_ALL}\n")
    while True:
        user_input = input(f"{Fore.GREEN}{Style.BRIGHT}➜{Style.RESET_ALL} {Fore.LIGHTYELLOW_EX}Enter a command:{Style.RESET_ALL} ")
        command, *args = parse_input(user_input)
        output, is_exit = get_output_by_command(command, args, book, notebook)
        print(output)
        if is_exit:
            save_data(book)
            save_notes(notebook)
            break
