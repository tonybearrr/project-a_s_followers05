"""
Handler functions for the address book bot.

This module contains all the command handler functions that process
user commands and interact with the AddressBook and Record classes.
"""
# flake8: noqa: E501
import re
from datetime import datetime, date
from collections import Counter
from colorama import init, Fore, Style
from models.address_book import AddressBook
from models.record import Record
from models.notebook import NoteBook
from models.note import Note
from models.birthday import Birthday
from utils.table_formatters import format_contact_table, format_notes_table
from utils.confirmations import confirm_delete
from utils.help_formatter import _header_line, _section_line
from .decorators import input_error
from .commands import Command
# Sort direction constants
ASCENDING_KEYWORDS = ["a", "asc", "ascending"]
DESCENDING_KEYWORDS = ["d", "desc", "descending"]


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
        return f"❌ Error: {Fore.RED}[{Command.ADD_CONTACT}]{Style.RESET_ALL} command requires a {Fore.CYAN}name{Style.RESET_ALL} and a {Fore.GREEN}phone{Style.RESET_ALL} number."

    name = args[0]
    phone = args[1]
    record = book.find(name)
    is_not_found = record is None
    if is_not_found:
        record = Record(name)
        book.add_record(record)

    if record.find_phone(phone):
        return f"❌ Phone number {Fore.GREEN}{phone}{Style.RESET_ALL} already exists for contact {Fore.CYAN}{name}{Style.RESET_ALL}."

    record.add_phone(phone)
    status = "added" if is_not_found else "updated"
    return f"✅ Contact {Fore.CYAN}{name}{Style.RESET_ALL} with phone {Fore.GREEN}{phone}{Style.RESET_ALL} {status} successfully."


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
        return (
            f"❌ Error: {Fore.RED}[{Command.UPDATE_CONTACT}]{Style.RESET_ALL} command requires a {Fore.CYAN}name{Style.RESET_ALL}, "
            f"{Fore.YELLOW}old_phone{Style.RESET_ALL} and a {Fore.GREEN}new_phone{Style.RESET_ALL}."
        )
    name, old_phone, new_phone = args
    record = book.find(name)
    if not record:
        return f"❌ Contact {Fore.CYAN}{name}{Style.RESET_ALL} not found."
    record.edit_phone(old_phone, new_phone)
    return f"✅ Phone number for {Fore.CYAN}{name}{Style.RESET_ALL} updated from {Fore.YELLOW}{old_phone}{Style.RESET_ALL} to {Fore.GREEN}{new_phone}{Style.RESET_ALL}."


def get_all_contacts(book: AddressBook):
    """
    Get all contacts from the address book.

    Args:
        book (AddressBook): Address book instance

    Returns:
        str: Formatted list of all contacts or "No contacts found."
    """
    if not book.data:
        return "❌ No contacts found."
    return format_contact_table(book.data.values())


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
        return f"❌ Error: {Fore.RED}[{Command.SHOW_CONTACT}]{Style.RESET_ALL} command requires a {Fore.CYAN}name{Style.RESET_ALL}."
    name = args[0]
    record = book.find(name)
    if not record:
        return f"❌ Contact {Fore.CYAN}{name}{Style.RESET_ALL} not found."

    pattern = r"(\d{3})(\d{3})(\d{4})"
    replacement = r"(\1)\2-\3"

    phones = "; ".join((re.sub(pattern, replacement, p.value)) for p in record.phones) if record.phones else "no phones"
    return f"📞 {Fore.GREEN}{phones}{Style.RESET_ALL} - {Fore.CYAN}{record.name}{Style.RESET_ALL}"


def search_contacts(args, book: AddressBook):
    """
    Search the contacts from the address book.

    Args:
        book (AddressBook): Address book instance

    Returns:
        str: Formatted list of all contacts or "No contacts found."
    """
    if len(args) < 1:
        return f"❌ Error: [{Fore.RED}{Command.SEARCH_CONTACTS}{Style.RESET_ALL}] command requires a {Fore.CYAN}'value'{Style.RESET_ALL}."
    else:
        searchable_contacts = set()
        value = args[0]

        search_by_name = book.search_contacts_by_name(value)
        search_by_phone = book.search_contacts_by_phone(value)
        search_by_email = book.search_contacts_by_email(value)
        search_by_address = book.search_contacts_by_address(value)

        searchable_contacts = search_by_name.union(search_by_phone).union(search_by_email).union(search_by_address)

        if not searchable_contacts:
            return "❌ No contacts found."

        return format_contact_table(searchable_contacts, value)


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
        return f"❌ Error: {Fore.RED}[{Command.DELETE_CONTACT}]{Style.RESET_ALL} command requires a {Fore.CYAN}'name'{Style.RESET_ALL}."

    name = args[0]
    record = book.find(name)

    if not record:
        return f"❌ Contact {Fore.CYAN}'{name}'{Style.RESET_ALL} not found."

    if not confirm_delete("contact", name):
        return "❌ Deletion cancelled."

    book.delete(name)
    return f"✅ Contact {Fore.CYAN}'{name}'{Style.RESET_ALL} successfully deleted."


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
        return (
            f"❌ Error: {Fore.RED}[{Command.ADD_BIRTHDAY}]{Style.RESET_ALL} command requires a {Fore.CYAN}'name'{Style.RESET_ALL} and "
            f"a birthday {Fore.MAGENTA}'{Birthday.DATE_FORMAT_DISPLAY}'{Style.RESET_ALL}."
        )

    name, birthday, *_ = args
    record = book.find(name)
    if not record:
        return f"❌ Contact {Fore.CYAN}'{name}'{Style.RESET_ALL} not found."
    record.add_birthday(birthday)
    return f"✅ Birthday added for {Fore.CYAN}'{name}'{Style.RESET_ALL}: {Fore.MAGENTA}'{birthday}'{Style.RESET_ALL}"


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
        return f"❌ Error: {Fore.RED}[{Command.SHOW_BIRTHDAY}]{Style.RESET_ALL} command requires a {Fore.CYAN}'name'{Style.RESET_ALL}."
    name = args[0]
    if record := book.find(name):
        return (
            f"🎁 {Fore.CYAN}'{name}'{Style.RESET_ALL}'s birthday is {Fore.MAGENTA}'{record.birthday}'{Style.RESET_ALL}"
            if record.birthday
            else f"❌ {Fore.CYAN}'{name}'{Style.RESET_ALL} has no birthday set."
        )
    else:
        return f"❌ Contact {Fore.CYAN}'{name}'{Style.RESET_ALL} not found."


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
        return f"❌ Error: {Fore.RED}[{Command.ADD_EMAIL}]{Style.RESET_ALL} command requires a {Fore.CYAN}'name'{Style.RESET_ALL} and an {Fore.YELLOW}'email'{Style.RESET_ALL}."

    name, email = args
    record = book.find(name)
    if not record:
        return f"❌ Contact {Fore.CYAN}'{name}'{Style.RESET_ALL} not found."
    old_email = record.email.value if record.email else None
    record.add_email(email)
    status = "updated" if old_email else "added"
    return f"✅ Email {Fore.YELLOW}'{email}'{Style.RESET_ALL} {status} for contact {Fore.CYAN}'{name}'{Style.RESET_ALL}."


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
        return f"❌ Error: {Fore.RED}[{Command.DELETE_EMAIL}]{Style.RESET_ALL} command requires a {Fore.CYAN}'name'{Style.RESET_ALL}."

    name = args[0]
    record = book.find(name)
    if not record:
        return f"❌ Contact {Fore.CYAN}'{name}'{Style.RESET_ALL} not found."
    if not record.email:
        return f"❌ Contact {Fore.CYAN}'{name}'{Style.RESET_ALL} has no {Fore.YELLOW}'email'{Style.RESET_ALL} to delete."
    record.delete_email()
    return f"✅ Email successfully removed from contact {Fore.CYAN}'{name}'{Style.RESET_ALL}."


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
        return f"❌ Error: {Fore.RED}[{Command.SHOW_EMAIL}]{Style.RESET_ALL} command requires a {Fore.CYAN}'name'{Style.RESET_ALL}."

    name = args[0]
    record = book.find(name)
    if not record:
        return f"❌ Contact {Fore.CYAN}'{name}'{Style.RESET_ALL} not found."
    email = record.email.value if record.email else "no email"
    return f"📧 {Fore.YELLOW}'{email}'{Style.RESET_ALL} - {Fore.CYAN}'{name}'{Style.RESET_ALL} "


@input_error
def show_upcoming_birthdays(args, book: AddressBook):
    """
    Get upcoming birthdays in the next days_ahead days.

    Args:
        args (list): Command arguments [days_ahead] (optional, default: 7)
        book (AddressBook): Address book instance

    Returns:
        str: Formatted list of upcoming birthdays or message if none found
    """
    days_ahead = _parse_days_ahead(args)
    if days_ahead is None:
        return (
            f"❌ Error: Please input valid number for "
            f"{Fore.RED}'{Command.SHOW_UPCOMING_BIRTHDAYS}'{Style.RESET_ALL} command"
        )

    upcoming = book.get_upcoming_birthdays(days_ahead=days_ahead)
    if not upcoming:
        return (
            f" {Style.BRIGHT}No {Fore.MAGENTA}birthdays{Style.RESET_ALL} "
            f"in the next {Fore.CYAN}{days_ahead}{Style.RESET_ALL} days."
        )

    today = date.today()
    lines = []

    for name, birthday_str in upcoming:
        # Convert date object to string if needed
        if isinstance(birthday_str, date):
            birthday_str = birthday_str.strftime("%d.%m.%Y")

        # Use existing helper functions
        bday_date, _, age = _calculate_birthday_info(birthday_str, today)
        formatted_entry = _format_upcoming_birthday(name, birthday_str, bday_date, age)
        lines.append(formatted_entry)

    return "\n".join(lines)


def _parse_days_ahead(args: list) -> int | None:
    """
    Parse days_ahead argument from command args.
    
    Args:
        args: Command arguments list
        
    Returns:
        int: Number of days ahead (default: 7), or None if invalid
    """
    if not args:
        return 7

    try:
        days = int(args[0])
        return days if days >= 0 else None
    except (ValueError, IndexError):
        return None


def _format_upcoming_birthday(name: str, birthday_str: str, 
                                     bday_date: date | None, age: int | None) -> str:
    """
    Format upcoming birthday entry (simpler version without days_until).
    
    Args:
        name: Contact name
        birthday_str: Original birthday string
        bday_date: Next birthday date
        age: Age that will be on birthday
        
    Returns:
        str: Formatted birthday entry
    """
    if bday_date:
        date_display = bday_date.strftime("%d.%m.%Y")
    else:
        date_display = birthday_str

    age_text = f" {Style.DIM}({age} years old){Style.RESET_ALL}" if age is not None else ""

    return (
        f"🎉 {Fore.MAGENTA}{date_display}{Style.RESET_ALL} - "
        f"{Fore.CYAN}{name}{Style.RESET_ALL}{age_text}"
    )

@input_error
def add_address(args, book: AddressBook):
    """
    Add address for a contact.

    Args:
        args (list): Command arguments [name, address]
        book (AddressBook): Address book instance

    Returns:
        str: Success message or error message
    """
    if len(args) < 2:
        return f"❌ Error: {Fore.RED}[{Command.ADD_ADDRESS}]{Style.RESET_ALL} command requires a {Fore.CYAN}'name'{Style.RESET_ALL} and an {Fore.BLUE}'address'{Style.RESET_ALL}."
    name, *address_parts = args
    address = " ".join(address_parts)
    record = book.find(name)
    if not record:
        return f"❌ Contact {Fore.CYAN}'{name}'{Style.RESET_ALL} not found."
    record.add_address(address)
    return f"✅ Address {Fore.BLUE}'{address}'{Style.RESET_ALL} for contact {Fore.CYAN}'{name}'{Style.RESET_ALL} added successfully."

@input_error
def edit_address(args, book: AddressBook):
    """
    Update address for a contact.

    Args:
        args (list): Command arguments [name, address]
        book (AddressBook): Address book instance

    Returns:
        str: Success message or error message
    """
    if len(args) < 2:
        return f"❌ Error: {Fore.RED}[{Command.CHANGE_ADDRESS}]{Style.RESET_ALL} command requires a {Fore.CYAN}'name'{Style.RESET_ALL} and a new {Fore.BLUE}'address'{Style.RESET_ALL}."
    name, *address_parts = args
    address = " ".join(address_parts)
    record = book.find(name)
    if not record:
        return f"❌ Contact {Fore.CYAN}'{name}'{Style.RESET_ALL} not found."
    record.edit_address(address)
    return f"✅ Address {Fore.BLUE}'{address}'{Style.RESET_ALL} for contact {Fore.CYAN}'{name}'{Style.RESET_ALL} changed successfully."


@input_error
def remove_address(args, book: AddressBook):
    """
    Delete address from a contact.

    Args:
        args (list): Command arguments [name]
        book (AddressBook): Address book instance

    Returns:
        str: Success message or error message
    """
    if len(args) < 1:
        return f"❌ Error: {Fore.RED}[{Command.DELETE_ADDRESS}]{Style.RESET_ALL} command requires a {Fore.CYAN}'name'{Style.RESET_ALL}."
    name = args[0]
    record = book.find(name)
    if not record:
        print(f"error {name}")
        return f"❌ Contact {Fore.CYAN}'{name}'{Style.RESET_ALL} not found."
    record.remove_address()
    return f"✅ Address successfully removed for contact {Fore.CYAN}'{name}'{Style.RESET_ALL}."

def parse_tags(tags_input):
    """
    Parse tags from input string or list, supporting comma or space as separators.

    Args:
        tags_input (str or list): Tags as string or list

    Returns:
        list: List of unique, non-empty tags
    """
    if isinstance(tags_input, str):
        tags = tags_input.replace(",", " ").split()
    elif isinstance(tags_input, list):
        tags_str = " ".join(str(tag) for tag in tags_input)
        tags = tags_str.replace(",", " ").split()
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
        raise ValueError(f"{Fore.RED}[{Command.ADD_NOTE}]{Style.RESET_ALL} command requires a {Fore.CYAN}'text'{Style.RESET_ALL}.")

    text = args[0]
    tags = parse_tags(args[1:]) if len(args) > 1 else []

    note = Note(text, tags)
    notebook.add_note(note)

    # Get note number (position in sorted list)
    all_notes = notebook.get_all_notes(sort_by="created",reverse=False)
    note_number = all_notes.index(note) + 1

    tags_str = f" with tags: {Fore.CYAN}{', '.join(tags)}{Style.RESET_ALL}" if tags else ""
    return f"✅ Note {Fore.GREEN}#{note_number}{Style.RESET_ALL} added{tags_str}."


@input_error
def search_notes(args, notebook: NoteBook):
    """
    Search notes by text or tags.

    Args:
        args (list): Command arguments [query]
        notebook (NoteBook): Notebook instance

    Returns:
        str: Formatted table of matching notes
    """
    if not args:
        raise ValueError("Search query is required")

    query = args[0]
    results = notebook.search_notes(query)

    if not results:
        return (
            f"❌ No {Fore.GREEN}notes{Style.RESET_ALL} found matching "
            f"{Fore.CYAN}'{query}'{Style.RESET_ALL}."
        )

    sort_by = "created"
    reverse = True  # newest first
    sorted_results = sorted(results, key=lambda n: n.created_at, reverse=reverse)

    all_notes = notebook.get_all_notes(sort_by=sort_by, reverse=reverse)
    note_to_number = {note: i + 1 for i, note in enumerate(all_notes)}
    sorted_results_with_numbers = sorted(
        sorted_results,
        key=lambda n: note_to_number.get(n, len(all_notes) + 1)
    )

    header = (
        f"{_section_line(Fore.CYAN)}\n"
        f"{Fore.CYAN}{Style.BRIGHT}Search results{Style.RESET_ALL} "
        f"{Fore.YELLOW}({len(results)} note(s) matching '{query}', sorted by creation date){Style.RESET_ALL}\n"
        f"{_section_line(Fore.CYAN)}\n"
    )

    table = format_notes_table(
        sorted_results_with_numbers, 
        sort_by=sort_by, 
        reverse=reverse,
        note_numbers=note_to_number
    )
    
    return header + table


@input_error
def search_notes_by_tags(args, notebook: NoteBook):
    """
    Search notes by tags (all specified tags must be present).

    Args:
        args (list): Command arguments [tag1, tag2] or [tag1,tag2]
        notebook (NoteBook): Notebook instance

    Returns:
        str: Formatted table of matching notes
    """
    if not args:
        raise ValueError(f"At least one {Fore.CYAN}tag{Style.RESET_ALL} is required")

    tags = parse_tags(args)

    if not tags:
        return f"❌ No valid {Fore.CYAN}tags{Style.RESET_ALL} provided."

    results = notebook.search_by_tags(tags)

    if not results:
        tags_str = ", ".join(tags)
        return (
            f"❌ No {Fore.GREEN}notes{Style.RESET_ALL} found with tags: "
            f"{Fore.CYAN}[{tags_str}]{Style.RESET_ALL}."
        )


    sort_by = "created"
    reverse = True
    sorted_results = sorted(results, key=lambda n: n.created_at, reverse=reverse)

    all_notes = notebook.get_all_notes(sort_by=sort_by, reverse=reverse)
    note_to_number = {note: i + 1 for i, note in enumerate(all_notes)}

    sorted_results_with_numbers = sorted(
        sorted_results,
        key=lambda n: note_to_number.get(n, len(all_notes) + 1)
    )

    tags_str = ", ".join(tags)
    header = (
        f"{_section_line(Fore.CYAN)}\n"
        f"{Fore.CYAN}{Style.BRIGHT}Search results by tags{Style.RESET_ALL} "
        f"{Fore.YELLOW}({len(results)} note(s) with tags [{tags_str}], sorted by creation date){Style.RESET_ALL}\n"
        f"{_section_line(Fore.CYAN)}\n"
    )

    table = format_notes_table(
        sorted_results_with_numbers, 
        sort_by=sort_by, 
        reverse=reverse,
        note_numbers=note_to_number
    )

    return header + table


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
        raise ValueError(f"{Fore.RED}[{Command.EDIT_NOTE}]{Style.RESET_ALL} command requires a {Fore.CYAN}identifier{Style.RESET_ALL} and a {Fore.WHITE}'new_text'{Style.RESET_ALL}.")

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
        return f"❌ Note {Fore.CYAN}#{identifier}{Style.RESET_ALL} not found."

    # Update note
    note.text = new_text
    note.updated_at = __import__("datetime").datetime.now()
    note.edit_tags(new_tags)

    tags_str = f" with tags: {Fore.CYAN}{', '.join(new_tags)}{Style.RESET_ALL}" if new_tags else " (no tags)"
    return f"✅ Note {Fore.GREEN}#{identifier}{Style.RESET_ALL} updated{tags_str} successfully."


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
        raise ValueError(f"{Fore.RED}[{Command.DELETE_NOTE}]{Style.RESET_ALL} command requires an {Fore.CYAN}identifier{Style.RESET_ALL}.")

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
        return f"❌ Note {Fore.CYAN}#{identifier}{Style.RESET_ALL} not found."

    if not confirm_delete("note", f"#{identifier}"):
        return f"❌ {Style.DIM}Deletion cancelled.{Style.RESET_ALL}"

    # Delete note
    deleted = notebook.delete_note(note_id)

    if deleted:
        return f"✅ Note {Fore.GREEN}#{identifier}{Style.RESET_ALL} deleted successfully."
    return "❌ Failed to delete note."

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
    sort_by = "created"
    reverse = None

    if args:
        # Parse sort column
        if args[0].startswith("sort="):
            sort_by = args[0].split("=", 1)[1]
        elif args[0] in ["created", "updated", "text", "tags"]:
            sort_by = args[0]

        # Parse sort direction (a=asc, d=desc)
        if len(args) > 1:
            if args[1].lower() in ASCENDING_KEYWORDS:
                reverse = False
            elif args[1].lower() in DESCENDING_KEYWORDS:
                reverse = True
        elif len(args) == 1 and args[0].lower() in ASCENDING_KEYWORDS + DESCENDING_KEYWORDS:
            # If only direction is provided, use default sort_by
            if args[0].lower() in ASCENDING_KEYWORDS:
                reverse = False
            elif args[0].lower() in DESCENDING_KEYWORDS:
                reverse = True

    notes = notebook.get_all_notes(sort_by=sort_by, reverse=reverse)

    if not notes:
        return "❌ No notes found."

    sort_labels = {
        "created": "by creation date",
        "updated": "by update date",
        "text": "alphabetically",
        "tags": "by tags",
    }

    # Determine sort direction for display
    if reverse is None:
        # Auto-determined: use defaults based on sort_by
        if sort_by in ["text", "tags"]:
            actual_reverse = False  # A-Z for text/tags
        else:
            actual_reverse = True  # newest first for created/updated
    else:
        actual_reverse = reverse

    sort_direction = "descending" if actual_reverse else "ascending"
    sort_info = f"{sort_labels.get(sort_by, sort_by)} ({sort_direction})"
    header = (
        f"{_section_line(Fore.CYAN)}\n"
        f"{Fore.CYAN}{Style.BRIGHT}All notes{Style.RESET_ALL} "
        f"{Fore.YELLOW}(sorted {sort_info}){Style.RESET_ALL}\n"
        f"{_section_line(Fore.CYAN)}\n"
    )
    table = format_notes_table(notes, sort_by=sort_by, reverse=actual_reverse)
    return header + table


def _get_contacts_statistics(book: AddressBook) -> list[str]:
    """
    Get contacts statistics.

    Args:
        book: AddressBook instance

    Returns:
        list[str]: List of formatted contact statistics lines
    """
    total_contacts = len(book.data)
    return [f"{Fore.YELLOW}{Style.BRIGHT}📇 CONTACTS:{Style.RESET_ALL} {Fore.CYAN}{total_contacts}{Style.RESET_ALL}"]


def _get_notes_statistics(notebook: NoteBook) -> list[str]:
    """
    Get notes statistics including top tags.

    Args:
        notebook: NoteBook instance

    Returns:
        list[str]: List of formatted note statistics lines
    """
    all_notes = notebook.get_all_notes()
    total_notes = len(all_notes)

    stats = [f"{Fore.YELLOW}{Style.BRIGHT}📝 NOTES:{Style.RESET_ALL} {Fore.CYAN}{total_notes}{Style.RESET_ALL}"]

    # Collect all tags
    all_tags = []
    for note in all_notes:
        all_tags.extend(note.tags)

    tag_counts = Counter(all_tags)
    top_tags = tag_counts.most_common(3)

    if top_tags:
        stats.append(f"{Fore.YELLOW}🔝 TOP 3 TAGS:{Style.RESET_ALL}")
        for i, (tag, count) in enumerate(top_tags, 1):
            stats.append(
                f"    {Fore.CYAN}{i}.{Style.RESET_ALL} {Fore.GREEN}{tag}{Style.RESET_ALL} "
                f"({Fore.BLUE}{count}{Style.RESET_ALL} notes)"
            )

    return stats


def _calculate_birthday_info(birthday_str: str, today: date) -> tuple[date | None, int | None, int | None]:
    """
    Calculate birthday information: next occurrence date, days until, and age.

    Args:
        birthday_str: Birthday string in DD.MM.YYYY format
        today: Current date

    Returns:
        tuple: (next_birthday_date, days_until, age) or (None, None, None) if parsing fails
    """
    try:
        bday_parts = birthday_str.split('.')
        if len(bday_parts) == 3:
            day, month, birth_year = int(bday_parts[0]), int(bday_parts[1]), int(bday_parts[2])
            this_year_birthday = date(today.year, month, day)

            if this_year_birthday < today:
                this_year_birthday = date(today.year + 1, month, day)

            days_until = (this_year_birthday - today).days
            age = this_year_birthday.year - birth_year

            return (this_year_birthday, days_until, age)
    except (ValueError, IndexError):
        pass

    return (None, None, None)


def _format_birthday_entry(name: str, birthday_str: str, bday_date: date | None,
                           days_until: int | None, age: int | None) -> str:
    """
    Format a single birthday entry for display.

    Args:
        name: Contact name
        birthday_str: Original birthday string
        bday_date: Next birthday date
        days_until: Days until birthday
        age: Age that will be on birthday

    Returns:
        str: Formatted birthday entry
    """
    if days_until == 0:
        emoji = "🎉"
        days_text = f"{Fore.RED}{Style.BRIGHT}TODAY!{Style.RESET_ALL}"
    elif days_until == 1:
        emoji = "🎁"
        days_text = f"{Fore.YELLOW}{Style.BRIGHT}Tomorrow{Style.RESET_ALL}"
    elif days_until is not None and days_until <= 3:
        emoji = "🎈"
        days_text = f"{Fore.YELLOW}in {days_until} days{Style.RESET_ALL}"
    else:
        emoji = "📅"
        days_text = f"{Fore.CYAN}in {days_until} days{Style.RESET_ALL}" if days_until is not None else ""

    if bday_date:
        date_display = bday_date.strftime("%d.%m")
    else:
        date_display = birthday_str

    age_text = ""
    if age is not None:
        age_text = f" - {Fore.BLUE}will be {age} years old{Style.RESET_ALL}"

    return f"  {emoji} {Fore.GREEN}{name}{Style.RESET_ALL} - {Fore.MAGENTA}{date_display}{Style.RESET_ALL} ({days_text}){age_text}"


def _get_birthdays_statistics(book: AddressBook, days_ahead: int = 10) -> list[str]:
    """
    Get upcoming birthdays statistics.

    Args:
        book: AddressBook instance
        days_ahead: Number of days ahead to look for birthdays

    Returns:
        list[str]: List of formatted birthday statistics lines
    """
    stats = [f"{Fore.YELLOW}{Style.BRIGHT}🎂 UPCOMING BIRTHDAYS (next {days_ahead} days):{Style.RESET_ALL}"]

    upcoming = book.get_upcoming_birthdays(days_ahead=days_ahead)

    if not upcoming:
        stats.append(f"  {Fore.WHITE}No birthdays in the next {days_ahead} days{Style.RESET_ALL}")
        return stats

    today = datetime.now().date()
    birthday_list = []

    for name, birthday_str in upcoming:
        bday_date, days_until, age = _calculate_birthday_info(birthday_str, today)
        birthday_list.append((name, birthday_str, bday_date, days_until, age))

    # Sort by days until birthday
    birthday_list.sort(key=lambda x: x[3] if x[3] is not None else 999)

    for name, birthday_str, bday_date, days_until, age in birthday_list:
        formatted_entry = _format_birthday_entry(name, birthday_str, bday_date, days_until, age)
        stats.append(formatted_entry)

    return stats


def show_statistics(book: AddressBook, notebook: NoteBook):
    """
    Show comprehensive application statistics.

    Args:
        book: AddressBook instance
        notebook: NoteBook instance

    Returns:
        str: Formatted statistics
    """
    stats = []

    # Header
    stats.append(_header_line())
    stats.append(f"{Fore.CYAN}{' ' * 25}{Style.BRIGHT}📊 STATISTICS{Style.RESET_ALL}")
    stats.append(_header_line() + "\n")

    # Contacts statistics
    stats.extend(_get_contacts_statistics(book))

    # Notes statistics
    stats.extend(_get_notes_statistics(notebook))
    stats.append("")

    # Upcoming birthdays statistics
    stats.extend(_get_birthdays_statistics(book, days_ahead=10))
    stats.append("")

    # Footer
    stats.append(_header_line())

    return "\n".join(stats)
