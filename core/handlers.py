"""
Handler functions for the address book bot.

This module contains all the command handler functions that process
user commands and interact with the AddressBook and Record classes.
"""
from models.address_book import AddressBook
from models.record import Record
from models.notebook import NoteBook
from models.note import Note
from models.birthday import Birthday
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
        return (f"Error: [{Command.UPDATE_CONTACT}] command requires a name, "
                f"old phone number and a new phone number.")
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

def search_contacts(args, book: AddressBook):
    """
    Search the contacts from the address book.

    Args:
        book (AddressBook): Address book instance

    Returns:
        str: Formatted list of all contacts or "No contacts found."
    """
    if len(args) < 1:
        return f"Error: [{Command.DELETE_CONTACT}] command requires a value."
    else:
        searchable_contacts = set()
        value = args[0]

        search_by_name = book.search_contacts_by_name(value)
        search_by_phone = book.search_contacts_by_phone(value)
        search_by_email = book.search_contacts_by_email(value)
        # search_by_address = book.search_contacts_by_address(value)
        
        searchable_contacts = search_by_name.union(search_by_phone).union(search_by_email)
        
        if not searchable_contacts:
            return "No contacts found."
        return "\n".join(str(record) for record in searchable_contacts)

    
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
        return (f"Error: [{Command.ADD_BIRTHDAY}] command requires a name and "
                f"a birthday ({Birthday.DATE_FORMAT_DISPLAY}).")

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


@input_error
def add_email(args, book: AddressBook):
    """
    Add or update email address for a contact.

    Args:
        args (list): Command arguments [name, email]
        book (AddressBook): Address book instance

    Returns:
        str: Success message or error message
    """
    if len(args) < 2:
        return f"Error: [{Command.ADD_EMAIL}] command requires a name and an email address."

    name, email = args
    record = book.find(name)
    if not record:
        return f"Contact '{name}' not found."
    old_email = record.email.value if record.email else None
    record.add_email(email)
    status = "updated" if old_email else "added"
    return f"Email '{email}' {status} for contact '{name}'."


@input_error
def delete_email(args, book: AddressBook):
    """
    Delete email address from a contact.

    Args:
        args (list): Command arguments [name]
        book (AddressBook): Address book instance

    Returns:
        str: Success message or error message
    """
    if len(args) < 1:
        return f"Error: [{Command.DELETE_EMAIL}] command requires a name."

    name = args[0]
    record = book.find(name)
    if not record:
        return f"Contact '{name}' not found."
    if not record.email:
        return f"Contact '{name}' has no email to delete."
    record.delete_email()
    return f"Email deleted from contact '{name}'."


@input_error
def show_email(args, book: AddressBook):
    """
    Show a contact's email address.

    Args:
        args (list): Command arguments [name]
        book (AddressBook): Address book instance

    Returns:
        str: Contact name and email address or error message
    """
    if len(args) < 1:
        return f"Error: [{Command.SHOW_EMAIL}] command requires a name."

    name = args[0]
    record = book.find(name)
    if not record:
        return f"Contact '{name}' not found."
    email = record.email.value if record.email else "no email"
    return f"{name}: {email}"


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


def parse_tags(tags_input):
    """
    Parse tags from input string or list, supporting comma or space as separators.

    Args:
        tags_input (str or list): Tags as string or list

    Returns:
        list: List of unique, non-empty tags
    """
    if isinstance(tags_input, str):
        # Replace commas with spaces and split
        tags = tags_input.replace(',', ' ').split()
    elif isinstance(tags_input, list):
        # Join list items and parse again to handle mixed formats
        tags_str = ' '.join(str(tag) for tag in tags_input)
        tags = tags_str.replace(',', ' ').split()
    else:
        return []

    # Remove empty strings and duplicates while preserving order
    seen = set()
    result = []
    for tag in tags:
        tag = tag.strip()
        if tag and tag not in seen:
            seen.add(tag)
            result.append(tag)

    return result


@input_error
def add_note(args, notebook: NoteBook):
    """
    Add a new note with optional tags.

    Args:
        args (list): Command arguments [text, tags...]
        notebook (NoteBook): Notebook instance

    Returns:
        str: Success message with note number
    """
    if not args:
        raise ValueError("Note text is required")

    text = args[0]
    tags = parse_tags(args[1:]) if len(args) > 1 else []

    note = Note(text, tags)
    notebook.add_note(note)

    # Get note number (position in sorted list)
    all_notes = notebook.get_all_notes(sort_by="created")
    note_number = all_notes.index(note) + 1

    tags_str = f" with tags: {', '.join(tags)}" if tags else ""
    return f"Note #{note_number} added{tags_str}."


@input_error
def search_notes(args, notebook: NoteBook):
    """
    Search notes by text or tags.

    Args:
        args (list): Command arguments [query]
        notebook (NoteBook): Notebook instance

    Returns:
        str: Formatted list of matching notes
    """
    if not args:
        raise ValueError("Search query is required")

    query = args[0]
    results = notebook.search_notes(query)

    if not results:
        return f"No notes found matching '{query}'."

    # Get all notes for numbering
    all_notes = notebook.get_all_notes(sort_by="created")

    lines = [f"Found {len(results)} note(s):"]
    for note in results:
        note_number = all_notes.index(note) + 1
        lines.append(f"#{note_number}: {note}")

    return "\n".join(lines)


@input_error
def search_notes_by_tags(args, notebook: NoteBook):
    """
    Search notes by tags (all specified tags must be present).

    Args:
        args (list): Command arguments [tag1, tag2] or [tag1,tag2]
        notebook (NoteBook): Notebook instance

    Returns:
        str: Formatted list of matching notes
    """
    if not args:
        raise ValueError("At least one tag is required")

    tags = parse_tags(args)

    if not tags:
        return "No valid tags provided."

    results = notebook.search_by_tags(tags)

    if not results:
        tags_str = ', '.join(tags)
        return f"No notes found with tags: {tags_str}."

    # Get all notes for numbering
    all_notes = notebook.get_all_notes(sort_by="created")

    tags_str = ', '.join(tags)
    lines = [f"Found {len(results)} note(s) with tags [{tags_str}]:"]
    for note in results:
        note_number = all_notes.index(note) + 1
        lines.append(f"#{note_number}: {note}")

    return "\n".join(lines)


@input_error
def edit_note(args, notebook: NoteBook):
    """
    Edit a note's text and tags.

    Args:
        args (list): Command arguments [identifier, new_text, new_tags...]
        notebook (NoteBook): Notebook instance

    Returns:
        str: Success message
    """
    if len(args) < 2:
        raise ValueError("Identifier and new text are required")

    identifier = args[0]
    new_text = args[1]
    new_tags = parse_tags(args[2:]) if len(args) > 2 else []

    # Try to find note by number first
    note = None
    if identifier.isdigit():
        note_number = int(identifier)
        note = notebook.get_note_by_number(note_number, sort_by="created")
    else:
        # Search by text fragment
        note = notebook.find_note_by_text(identifier)

    if not note:
        return f"Note '{identifier}' not found."

    # Update note
    note.text = new_text
    note.updated_at = __import__('datetime').datetime.now()
    note.edit_tags(new_tags)

    tags_str = f" with tags: {', '.join(new_tags)}" if new_tags else " (no tags)"
    return f"Note updated{tags_str}."


@input_error
def delete_note(args, notebook: NoteBook):
    """
    Delete a note by number or text.

    Args:
        args (list): Command arguments [identifier]
        notebook (NoteBook): Notebook instance

    Returns:
        str: Success message
    """
    if not args:
        raise ValueError("Note identifier is required")

    identifier = args[0]

    # Try to find note by number first
    note = None
    if identifier.isdigit():
        note_number = int(identifier)
        note_id = notebook.get_note_id_by_number(note_number, sort_by="created")
        if note_id:
            note = notebook.get_note_by_number(note_number, sort_by="created")
    else:
        # Search by text fragment
        note = notebook.find_note_by_text(identifier)
        note_id = note._uuid if note else None

    if not note or not note_id:
        return f"Note '{identifier}' not found."

    # Delete note
    deleted = notebook.delete_note(note_id)

    if deleted:
        return f"Note deleted: {note.text[:50]}..."
    return "Failed to delete note."


@input_error
def list_notes(args, notebook: NoteBook):
    """
    List all notes with optional sorting.

    Args:
        args (list): Command arguments [sort=...] (optional)
        notebook (NoteBook): Notebook instance

    Returns:
        str: Formatted list of all notes
    """
    # Parse sort parameter
    sort_by = "created"  # default
    if args:
        if args[0].startswith("sort="):
            sort_by = args[0].split("=", 1)[1]
        elif args[0] in ["created", "updated", "text", "tags"]:
            sort_by = args[0]

    notes = notebook.get_all_notes(sort_by=sort_by)

    if not notes:
        return "No notes found."

    sort_labels = {
        "created": "by creation date",
        "updated": "by update date",
        "text": "alphabetically",
        "tags": "by tags"
    }

    lines = [f"All notes (sorted {sort_labels.get(sort_by, sort_by)}):"]
    for i, note in enumerate(notes, 1):
        lines.append(f"#{i}: {note}")

    return "\n".join(lines)
