"""
Address Book Bot - A command-line interface for managing contacts.

This module provides the main entry point for the address book bot,
which allows users to add, update, delete, and view contacts with
phone numbers and birthdays.
"""
from core.commands import Command
from models.Birthday import Birthday
from models.Phone import Phone
from core.handlers import (
    add_contact, update_contact, get_all_contacts, get_one_contact,
    delete_contact, add_birthday, show_birthday, birthdays
    delete_contact, add_birthday, show_birthday, birthdays, load_data,
    save_data,
    add_note, list_notes, search_notes, search_notes_by_tags,
    edit_note, delete_note, load_notes, save_notes
)
from utils.parsers import parse_input
from storage.file_storage import load_data, save_data


def get_output_by_command(command, args, book):
    """
    Main function that runs the address book bot.

    Creates an AddressBook and NoteBook instances and runs the main command loop,
    processing user commands until 'close' or 'exit' is entered.
    """
    is_exit = False
    if command in (Command.EXIT_1, Command.EXIT_2):
        is_exit = True
        output = "Good bye!"
    elif command == Command.HELLO:
        output = "How can I help you?"
    elif command == Command.ADD_CONTACT:
        output = add_contact(args, book)
    elif command == Command.UPDATE_CONTACT:
        output = update_contact(args, book)
    elif command == Command.SHOW_ALL_CONTACTS:
        output = get_all_contacts(book)
    elif command == Command.SHOW_CONTACT:
        output = get_one_contact(args, book)
    elif command == Command.DELETE_CONTACT:
        output = delete_contact(args, book)
    elif command == Command.ADD_BIRTHDAY:
        output = add_birthday(args, book)
    elif command == Command.SHOW_BIRTHDAY:
        output = show_birthday(args, book)
    elif command == Command.SHOW_UPCOMING_BIRTHDAYS:
        output = birthdays(book)
    elif command == Command.HELP or command == Command.HELP_ALT:
        output = (
            "Available commands:\n"
            f"{Command.HELLO} - Greet the bot\n"
            f"""{Command.ADD_CONTACT} <name> <phone> - Add a new contact.
            Expected phone lenght is {Phone.PHONE_LEN} digits.\n"""
            f"""{Command.UPDATE_CONTACT} <name> <old_phone> <new_phone> -
            Change an existing contact's phone number. Expected phone lenght
             is {Phone.PHONE_LEN} digits.\n"""
            f"{Command.SHOW_CONTACT} <name> - Show the phone number of a contact\n"
            f"{Command.SHOW_ALL_CONTACTS} - Show all contacts\n"
            f"""{Command.ADD_BIRTHDAY} <name> <{Birthday.DATE_FORMAT_DISPLAY}> -
            Add birthday to a contact\n"""
            f"{Command.SHOW_BIRTHDAY} <name> - Show birthday of a contact\n"
            f"{Command.SHOW_UPCOMING_BIRTHDAYS} - Show contacts with upcoming birthdays\n"
            f"{Command.EXIT_1}, {Command.EXIT_2} - Exit the program"
        )
    else:
        output = "Unknown command. Please try again."
    return output, is_exit


if __name__ == "__main__":
    book = load_data()
    notebook = load_notes()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)
        output, is_exit = get_output_by_command(command, args, book)
        print(output)
        if is_exit:
            save_data(book)
            break
