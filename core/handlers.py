"""
Handler functions for the address book bot.

This module contains all the command handler functions that process
user commands and interact with the AddressBook and Record classes.
"""
from models.AddressBook import AddressBook
from models.Record import Record
from models.Birthday import Birthday
from .decorators import input_error
from .commands import Command


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
    if len(args) < 2:
        return f"Error: [{Command.ADD_CONTACT}] command requires a name and a phone number."

    name = args[0]
    phone = args[1]
    record = book.find(name)
    is_not_found = record is None
    if is_not_found:
        record = Record(name)
        book.add_record(record)
    record.add_phone(phone)
    status = "added" if is_not_found else "updated"
    return f"Contact '{name}' with phone '{phone}' {status} successfully."


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
    if len(args) < 3:
        return f"Error: [{Command.UPDATE_CONTACT}] command requires a name, old phone number and a new phone number."
    name, old_phone, new_phone = args
    record = book.find(name)
    if not record:
        return f"Contact '{name}' not found."
    record.edit_phone(old_phone, new_phone)
    return f"Phone number for {name} updated from {old_phone} to {new_phone}."


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
    if len(args) < 1:
        return f"Error: [{Command.SHOW_CONTACT}] command requires a name."
    name = args[0]
    record = book.find(name)
    if not record:
        return f"Contact '{name}' not found."
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
    if len(args) < 1:
        return f"Error: [{Command.DELETE_CONTACT}] command requires a name."
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
    if len(args) < 2:
        return f"Error: [{Command.ADD_BIRTHDAY}] command requires a name and a birthday ({Birthday.DATE_FORMAT_DISPLAY})."

    name, bday, *_ = args
    record = book.find(name)
    if not record:
        return f"Contact '{name}' not found."
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
    if len(args) < 1:
        return f"Error: [{Command.SHOW_BIRTHDAY}] command requires a name."
    name = args[0]
    record = book.find(name)
    if not record:
        return f"Contact '{name}' not found."
    if record.birthday:
        return f"{name}'s birthday is {record.birthday}"
    return f"{name} has no birthday set."


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
