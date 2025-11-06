"""
Address Book Bot - A command-line interface for managing contacts.

This module provides the main entry point for the address book bot,
which allows users to add, update, delete, and view contacts with
phone numbers and birthdays.
"""
from models.birthday import Birthday
from models.phone import Phone
from core.commands import Command
from core.handlers import (
    add_contact, update_contact, get_all_contacts, get_one_contact,
    delete_contact, add_birthday, show_birthday, show_upcoming_birthdays,
    add_note, list_notes, search_notes, search_notes_by_tags,
    edit_note, delete_note, add_email, delete_email, show_email,
    add_address, edit_address, remove_address
)
from utils.parsers import parse_input
from storage.file_storage import load_data, save_data, load_notes, save_notes


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
        command_output = "Goodbye!"
    elif command == Command.HELLO:
        command_output = "How can I help you?"
    elif command == Command.ADD_CONTACT:
        command_output = add_contact(args, book)
    elif command == Command.UPDATE_CONTACT:
        command_output = update_contact(args, book)
    elif command == Command.SHOW_ALL_CONTACTS:
        command_output = get_all_contacts(book)
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
    elif command == Command.ADD_ADDRESS:
        command_output = add_address(args, notebook)
    elif command == Command.CHANGE_ADDRESS:
        command_output = edit_address(args, notebook)
    elif command == Command.REMOVE_ADDRESS:
        command_output = remove_address(args, notebook)
    elif command in [Command.HELP, Command.HELP_ALT]:
        command_output = (
            "\n"
            "Available commands:\n"
            "\n"
            f"{Command.HELLO} - Greet the bot\n"
            f"{Command.ADD_CONTACT} <name> <phone> - Add a new contact. "
            f"Expected phone length is {Phone.PHONE_LEN} digits.\n"
            f"{Command.UPDATE_CONTACT} <name> <old_phone> <new_phone> - "
            f"Change an existing contact's phone number. "
            f"Expected phone length is {Phone.PHONE_LEN} digits.\n"
            f"{Command.SHOW_CONTACT} <name> - Show the phone number of a contact\n"
            f"{Command.SHOW_ALL_CONTACTS} - Show all contacts\n"
            "\n"
            f"{Command.ADD_BIRTHDAY} <name> <{Birthday.DATE_FORMAT_DISPLAY}> - "
            f"Add birthday to a contact\n"
            f"{Command.SHOW_BIRTHDAY} <name> - Show birthday of a contact\n"
            f"{Command.SHOW_UPCOMING_BIRTHDAYS} [days_ahead_number]- Show contacts for upcoming birthdays."
            f" [days_ahead_number] parameter is optional, default is 7.\n"
            "\n"
            f"{Command.ADD_EMAIL} <name> <email> - Add or update email address for a contact\n"
            f"{Command.DELETE_EMAIL} <name> - Delete email address from a contact\n"
            f"{Command.SHOW_EMAIL} <name> - Show contact's email address\n"
            "\n"
            f"{Command.ADD_NOTE} <text> [tags] - Add a new note with optional tags\n"
            f"{Command.LIST_NOTES} [sort] - List all notes (sort: created/updated/text/tags)\n"
            f"{Command.SEARCH_NOTES} <query> - Search notes by text or tags\n"
            f"{Command.SEARCH_TAGS} <tags> - Search notes by specific tags\n"
            f"{Command.EDIT_NOTE} <identifier> <text> [tags] - Edit a note\n"
            f"{Command.DELETE_NOTE} <identifier> - Delete a note\n"
            "\n"
            "\n"
            f"{Command.ADD_ADDRESS} <name> [address] - Add an address for a contact\n"
            f"{Command.CHANGE_ADDRESS} <name> [address] - Change an address for a contact\n"
            f"{Command.REMOVE_ADDRESS} <name> - Remove an address for a contact\n"
            "\n"
            f"{Command.EXIT_1}, {Command.EXIT_2} - Exit the program"
        )
    else:
        command_output = "Unknown command. Please try again."
    return command_output, is_break_main_loop


if __name__ == "__main__":
    book = load_data()
    notebook = load_notes()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)
        output, is_exit = get_output_by_command(command, args, book, notebook)
        print(output)
        if is_exit:
            save_data(book)
            save_notes(notebook)
            break
