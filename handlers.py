"""
Handler functions for the address book bot.

This module contains all the command handler functions that process
user commands and interact with the AddressBook and Record classes.
"""
import pickle
from decorators import input_error
from models.AddressBook import AddressBook
from models.Record import Record


@input_error
def add_contact(args, book: AddressBook):
    """
    Add a new contact or update existing contact with phone number.

    Args:
        args (list): Command arguments [name, phone]
        book (AddressBook): Address book instance

    Returns:
        str: Success message or error message
    """
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated"
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added"
    if phone:
        try:
            record.add_phone(phone)
        except ValueError as e:
            return str(e)
    return message


@input_error
def update_contact(args, book: AddressBook):
    """
    Update a contact's phone number.

    Args:
        args (list): Command arguments [name, old_phone, new_phone]
        book (AddressBook): Address book instance

    Returns:
        str: Success message or error message
    """
    name, old_phone, new_phone = args
    record = book.find(name)
    try:
        record.edit_phone(old_phone, new_phone)
        return f"Phone number for {name} updated from {old_phone} to {new_phone}."
    except ValueError as e:
        return str(e)


@input_error
def get_all_contacts(book: AddressBook):
    """
    Get all contacts from the address book.

    Args:
        book (AddressBook): Address book instance

    Returns:
        str: Formatted list of all contacts or "No contacts found."
    """
    if not book.data:
        return "No contacts found."
    return "\n".join(str(record) for record in book.data.values())


@input_error
def get_one_contact(args, book: AddressBook):
    """
    Get a specific contact's phone numbers.
    Args:
        args (list): Command arguments [name]
        book (AddressBook): Address book instance

    Returns:
        str: Contact name and phone numbers or error message
    """
    name = args[0]
    record = book.find(name)
    phones = "; ".join(p.value for p in record.phones) if record.phones else "no phones"
    return f"{name}: {phones}"


@input_error
def delete_contact(args, book: AddressBook):
    """
    Delete a contact from the address book.

    Args:
        args (list): Command arguments [name]
        book (AddressBook): Address book instance

    Returns:
        str: Success message or error message
    """
    name = args[0]
    book.delete(name)
    return f"Contact '{name}' deleted."


@input_error
def add_birthday(args, book: AddressBook):
    """
    Add birthday to a contact.

    Args:
        args (list): Command arguments [name, birthday]
        book (AddressBook): Address book instance

    Returns:
        str: Success message or error message
    """
    name, bday, *_ = args
    record = book.find(name)
    record.add_birthday(bday)
    return f"Birthday added for {name}: {bday}"


@input_error
def show_birthday(args, book: AddressBook):
    """
    Show a contact's birthday.

    Args:
        args (list): Command arguments [name]
        book (AddressBook): Address book instance

    Returns:
        str: Birthday information or error message
    """
    name = args[0]
    record = book.find(name)
    if record.birthday:
        return f"{name}'s birthday is {record.birthday}"
    return f"{name} has no birthday set."


@input_error
def birthdays(book: AddressBook):
    """
    Get upcoming birthdays in the next 7 days.

    Args:
        book (AddressBook): Address book instance

    Returns:
        str: List of upcoming birthdays or "No birthdays in the next 7 days."
    """
    upcoming = book.get_upcoming_birthdays()
    if not upcoming:
        return "No birthdays in the next 7 days."
    lines = [f"{name}: {bday}" for name, bday in upcoming]
    return "\n".join(lines)


def save_data(book, filename="addressbook.pkl"):
    """
    Save the address book to a file.

    Args:
        book (AddressBook): Address book instance
        filename (str): Name of the file to save to
    """
    with open(filename, "wb") as f:
        pickle.dump(book, f)


def load_data(filename="addressbook.pkl"):
    """
    Load the address book from a file.

    Args:
        filename (str): Name of the file to load from

    Returns:
        AddressBook: Address book instance
    """
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()
