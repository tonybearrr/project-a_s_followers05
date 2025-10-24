"""
Address Book Bot - A command-line interface for managing contacts.

This module provides the main entry point for the address book bot,
which allows users to add, update, delete, and view contacts with
phone numbers and birthdays.
"""

from handlers import (
    add_contact, update_contact, get_all_contacts, get_one_contact,
    delete_contact, add_birthday, show_birthday, birthdays, load_data,
    save_data
)
from decorators import input_error


@input_error
def parse_input(user_input):
    """
    Parse user input into command and arguments.

    Args:
        user_input (str): Raw user input string

    Returns:
        tuple: Command and arguments (cmd, *args)
    """
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


def main():
    """
    Main function that runs the address book bot.

    Creates an AddressBook instance and runs the main command loop,
    processing user commands until 'close' or 'exit' is entered.
    """
    book = load_data()
    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            save_data(book)
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(update_contact(args, book))
        elif command == "all":
            print(get_all_contacts(book))
        elif command == "phone":
            print(get_one_contact(args, book))
        elif command == "delete":
            print(delete_contact(args, book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(book))
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
