"""
Tests for the handlers module.

This module contains tests for all handler functions in the address book bot.
"""

from datetime import date, timedelta
import time
from core.handlers import (
    add_contact,
    update_contact,
    get_all_contacts,
    get_one_contact,
    delete_contact,
    add_birthday,
    show_birthday,
    show_upcoming_birthdays,
    parse_tags,
    add_note,
    search_notes,
    search_notes_by_tags,
    edit_note,
    delete_note,
    list_notes,
    add_email,
    delete_email,
    show_email,
)
from models.address_book import AddressBook
from models.notebook import NoteBook
from models.record import Record


class TestAddContact:
    """Test suite for the add_contact handler."""

    def test_add_new_contact(self):
        """Test adding a new contact."""
        book = AddressBook()
        result = add_contact(["John Doe", "1234567890"], book)
        assert "added successfully" in result.lower()
        assert "John Doe" in book.data

    def test_update_existing_contact_with_phone(self):
        """Test adding phone to existing contact."""
        book = AddressBook()
        record = Record("John Doe")
        book.add_record(record)
        result = add_contact(["John Doe", "1234567890"], book)
        assert "updated successfully" in result.lower()
        assert len(record.phones) == 1

    def test_add_contact_invalid_phone(self):
        """Test adding contact with invalid phone."""
        book = AddressBook()
        result = add_contact(["John Doe", "123"], book)
        assert "Phone number must be 10 digits" in result


class TestUpdateContact:
    """Test suite for the update_contact handler."""

    def test_update_contact_phone(self):
        """Test updating a contact's phone number."""
        book = AddressBook()
        record = Record("John Doe")
        record.add_phone("1234567890")
        book.add_record(record)
        result = update_contact(["John Doe", "1234567890", "9876543210"], book)
        assert "updated" in result.lower()
        assert record.phones[0].value == "9876543210"

    def test_update_contact_phone_not_found(self):
        """Test updating non-existent phone."""
        book = AddressBook()
        record = Record("John Doe")
        record.add_phone("1234567890")
        book.add_record(record)
        result = update_contact(["John Doe", "9999999999", "1111111111"], book)
        assert "not found" in result.lower()

    def test_update_contact_invalid_new_phone(self):
        """Test updating with invalid new phone format."""
        book = AddressBook()
        record = Record("John Doe")
        record.add_phone("1234567890")
        book.add_record(record)
        result = update_contact(["John Doe", "1234567890", "123"], book)
        assert "Phone number must be 10 digits" in result


class TestGetAllContacts:
    """Test suite for the get_all_contacts handler."""

    def test_get_all_contacts_empty_book(self):
        """Test getting all contacts from empty book."""
        book = AddressBook()
        result = get_all_contacts(book)
        assert result == "No contacts found."

    def test_get_all_contacts_with_data(self):
        """Test getting all contacts."""
        book = AddressBook()
        record1 = Record("John Doe")
        record2 = Record("Jane Smith")
        book.add_record(record1)
        book.add_record(record2)
        result = get_all_contacts(book)
        assert "John Doe" in result
        assert "Jane Smith" in result


class TestGetOneContact:
    """Test suite for the get_one_contact handler."""

    def test_get_one_contact_with_phones(self):
        """Test getting a specific contact."""
        book = AddressBook()
        record = Record("John Doe")
        record.add_phone("1234567890")
        record.add_phone("0987654321")
        book.add_record(record)
        result = get_one_contact(["John Doe"], book)
        assert "John Doe" in result
        assert "1234567890" in result

    def test_get_one_contact_no_phones(self):
        """Test getting contact without phones."""
        book = AddressBook()
        record = Record("John Doe")
        book.add_record(record)
        result = get_one_contact(["John Doe"], book)
        assert "John Doe" in result
        assert "no phones" in result


class TestDeleteContact:
    """Test suite for the delete_contact handler."""

    def test_delete_existing_contact(self):
        """Test deleting an existing contact."""
        book = AddressBook()
        record = Record("John Doe")
        book.add_record(record)
        result = delete_contact(["John Doe"], book)
        assert "deleted" in result.lower()
        assert "John Doe" not in book.data

    def test_delete_non_existing_contact(self):
        """Test deleting non-existing contact raises error."""
        book = AddressBook()
        result = delete_contact(["Jane Doe"], book)
        assert "Contact not found" in result


class TestAddBirthday:
    """Test suite for the add_birthday handler."""

    def test_add_birthday_to_contact(self):
        """Test adding birthday to a contact."""
        book = AddressBook()
        record = Record("John Doe")
        book.add_record(record)
        result = add_birthday(["John Doe", "15.03.1990"], book)
        assert "Birthday added" in result
        assert record.birthday is not None

    def test_add_invalid_birthday_format(self):
        """Test adding birthday with invalid format."""
        book = AddressBook()
        record = Record("John Doe")
        book.add_record(record)
        result = add_birthday(["John Doe", "1990-03-15"], book)
        # Decoration catches the error and returns a generic message
        assert (
            "Enter the argument for the command" in result
            or "Invalid date format" in result
        )


class TestShowBirthday:
    """Test suite for the show_birthday handler."""

    def test_show_birthday_with_birthday(self):
        """Test showing birthday for contact with birthday."""
        book = AddressBook()
        record = Record("John Doe")
        record.add_birthday("15.03.1990")
        book.add_record(record)
        result = show_birthday(["John Doe"], book)
        assert "birthday is" in result
        assert "15.03.1990" in result

    def test_show_birthday_without_birthday(self):
        """Test showing birthday for contact without birthday."""
        book = AddressBook()
        record = Record("John Doe")
        book.add_record(record)
        result = show_birthday(["John Doe"], book)
        assert "no birthday set" in result


class TestBirthdays:
    """Test suite for the birthdays handler."""

    def test_no_upcoming_by_default(self):
        """Test birthdays when the contacts book is empty."""
        book = AddressBook()
        result = show_upcoming_birthdays([], book)
        assert result == "No birthdays in the next 7 days."

    def test_birthdays_no_upcoming(self):
        """Test birthdays when no upcoming birthdays."""
        book = AddressBook()
        result = show_upcoming_birthdays(["8"], book)
        assert "No birthdays in the next 8 days" in result

    def test_custom_days_argument_finds_upcoming(self):
        """Test birthdays for specific days ahead."""
        book = AddressBook()
        today = date.today()
        future_birthday = (today + timedelta(days=3)).strftime("%d.%m.%Y")
        record = Record("John Doe")
        record.add_birthday(future_birthday)
        book.add_record(record)

        result = show_upcoming_birthdays(["5"], book)
        assert "John Doe" in result

    def test_invalid_days_argument_returns_error_message(self):
        """Test birthdays when specific days ahead is not a number."""
        book = AddressBook()
        result = show_upcoming_birthdays(["not_a_number"], book)
        assert "Please input valid number" in result


class TestParseTags:
    """Test suite for the parse_tags function."""

    def test_parse_tags_comma_separated(self):
        """Test parsing comma-separated tags."""
        result = parse_tags("tag1,tag2,tag3")
        assert result == ["tag1", "tag2", "tag3"]

    def test_parse_tags_space_separated(self):
        """Test parsing space-separated tags."""
        result = parse_tags("tag1 tag2 tag3")
        assert result == ["tag1", "tag2", "tag3"]

    def test_parse_tags_mixed_separators(self):
        """Test parsing mixed comma and space separators."""
        result = parse_tags("tag1, tag2 tag3,tag4")
        assert result == ["tag1", "tag2", "tag3", "tag4"]

    def test_parse_tags_removes_duplicates(self):
        """Test that duplicates are removed."""
        result = parse_tags("tag1,tag2,tag1,tag3,tag2")
        assert result == ["tag1", "tag2", "tag3"]

    def test_parse_tags_removes_empty(self):
        """Test that empty tags are removed."""
        result = parse_tags("tag1,,tag2,  ,tag3")
        assert result == ["tag1", "tag2", "tag3"]

    def test_parse_tags_from_list(self):
        """Test parsing from a list."""
        result = parse_tags(["tag1", "tag2", "tag3"])
        assert result == ["tag1", "tag2", "tag3"]

    def test_parse_tags_from_list_with_commas(self):
        """Test parsing from a list containing commas."""
        result = parse_tags(["tag1,tag2", "tag3"])
        assert result == ["tag1", "tag2", "tag3"]

    def test_parse_tags_empty_string(self):
        """Test parsing empty string."""
        result = parse_tags("")
        assert not result

    def test_parse_tags_empty_list(self):
        """Test parsing empty list."""
        result = parse_tags([])
        assert not result

    def test_parse_tags_whitespace_only(self):
        """Test parsing whitespace-only string."""
        result = parse_tags("   ,  ,  ")
        assert not result

    def test_parse_tags_with_extra_whitespace(self):
        """Test parsing with extra whitespace."""
        result = parse_tags("  tag1  ,  tag2  ,  tag3  ")
        assert result == ["tag1", "tag2", "tag3"]

    def test_parse_tags_invalid_type(self):
        """Test parsing with invalid type returns empty list."""
        result = parse_tags(123)
        assert not result

    def test_parse_tags_none(self):
        """Test parsing None returns empty list."""
        result = parse_tags(None)
        assert not result

    def test_parse_tags_with_numbers(self):
        """Test parsing list with numbers."""
        result = parse_tags([1, 2, 3])
        assert result == ["1", "2", "3"]

    def test_parse_tags_mixed_types_in_list(self):
        """Test parsing list with mixed types."""
        result = parse_tags(["tag1", 123, "tag2"])
        assert result == ["tag1", "123", "tag2"]


class TestAddNote:
    """Test suite for the add_note handler."""

    def test_add_note_text_only(self):
        """Test adding a note with text only."""
        notebook = NoteBook()
        result = add_note(["Test note"], notebook)
        assert "Note #1 added" in result
        assert len(notebook) == 1

    def test_add_note_with_single_tag(self):
        """Test adding a note with a single tag."""
        notebook = NoteBook()
        result = add_note(["Test note", "important"], notebook)
        assert "Note #1 added" in result
        assert "important" in result
        assert len(notebook) == 1

    def test_add_note_with_multiple_tags(self):
        """Test adding a note with multiple tags."""
        notebook = NoteBook()
        result = add_note(["Test note", "tag1,tag2,tag3"], notebook)
        assert "Note #1 added" in result
        assert "tag1" in result or "tags:" in result

    def test_add_note_with_space_separated_tags(self):
        """Test adding a note with space-separated tags."""
        notebook = NoteBook()
        result = add_note(["Test note", "tag1", "tag2", "tag3"], notebook)
        assert "Note #1 added" in result

    def test_add_note_empty_args(self):
        """Test adding note with empty args raises error."""
        notebook = NoteBook()
        result = add_note([], notebook)
        assert (
            "Note text is required" in result
            or "Enter the argument for the command" in result
        )

    def test_add_note_empty_text(self):
        """Test adding note with empty text."""
        notebook = NoteBook()
        result = add_note([""], notebook)
        assert (
            "Note text cannot be empty" in result
            or "Enter the argument for the command" in result
        )

    def test_add_note_whitespace_only_text(self):
        """Test adding note with whitespace-only text."""
        notebook = NoteBook()
        result = add_note(["   "], notebook)
        assert (
            "Note text cannot be empty" in result
            or "Enter the argument for the command" in result
        )

    def test_add_multiple_notes(self):
        """Test adding multiple notes."""
        notebook = NoteBook()
        add_note(["First note"], notebook)
        add_note(["Second note"], notebook)
        add_note(["Third note"], notebook)
        assert len(notebook) == 3

    def test_add_note_with_duplicate_tags(self):
        """Test that duplicate tags are removed."""
        notebook = NoteBook()
        result = add_note(["Test note", "tag1,tag1,tag2"], notebook)
        assert "Note #1 added" in result
        notes = notebook.get_all_notes()
        assert len(notes[0].tags) == 2

    def test_add_note_with_empty_tags(self):
        """Test adding note with empty tag strings."""
        notebook = NoteBook()
        result = add_note(["Test note", ",,"], notebook)
        assert "Note #1 added" in result


class TestSearchNotes:
    """Test suite for the search_notes handler."""

    def test_search_notes_by_text(self):
        """Test searching notes by text."""
        notebook = NoteBook()
        add_note(["Buy groceries"], notebook)
        add_note(["Call mom"], notebook)
        add_note(["Buy tickets"], notebook)

        result = search_notes(["buy"], notebook)
        assert "Found 2 note(s)" in result
        assert "groceries" in result or "tickets" in result

    def test_search_notes_by_tag(self):
        """Test searching notes by tag."""
        notebook = NoteBook()
        add_note(["Note 1", "important"], notebook)
        add_note(["Note 2", "urgent"], notebook)
        add_note(["Note 3", "important"], notebook)

        result = search_notes(["important"], notebook)
        assert "Found 2 note(s)" in result

    def test_search_notes_no_results(self):
        """Test searching with no matching results."""
        notebook = NoteBook()
        add_note(["Test note"], notebook)

        result = search_notes(["nonexistent"], notebook)
        assert "No notes found" in result

    def test_search_notes_empty_notebook(self):
        """Test searching in empty notebook."""
        notebook = NoteBook()
        result = search_notes(["anything"], notebook)
        assert "No notes found" in result

    def test_search_notes_empty_query(self):
        """Test searching with empty query."""
        notebook = NoteBook()
        result = search_notes([], notebook)
        assert (
            "Search query is required" in result
            or "Enter the argument for the command" in result
        )

    def test_search_notes_case_insensitive(self):
        """Test that search is case-insensitive."""
        notebook = NoteBook()
        add_note(["IMPORTANT NOTE"], notebook)

        result = search_notes(["important"], notebook)
        assert "Found 1 note(s)" in result

    def test_search_notes_partial_match(self):
        """Test searching with partial text match."""
        notebook = NoteBook()
        add_note(["Meeting tomorrow at 3pm"], notebook)

        result = search_notes(["tomorrow"], notebook)
        assert "Found 1 note(s)" in result

    def test_search_notes_shows_numbers(self):
        """Test that search results show note numbers."""
        notebook = NoteBook()
        add_note(["Test note 1"], notebook)
        add_note(["Test note 2"], notebook)

        result = search_notes(["Test"], notebook)
        assert "#1" in result or "#2" in result


class TestSearchNotesByTags:
    """Test suite for the search_notes_by_tags handler."""

    def test_search_by_single_tag(self):
        """Test searching by single tag."""
        notebook = NoteBook()
        add_note(["Note 1", "important"], notebook)
        add_note(["Note 2", "urgent"], notebook)
        add_note(["Note 3", "important"], notebook)

        result = search_notes_by_tags(["important"], notebook)
        assert "Found 2 note(s)" in result

    def test_search_by_multiple_tags_all_present(self):
        """Test searching by multiple tags - all must be present."""
        notebook = NoteBook()
        add_note(["Note 1", "important,work"], notebook)
        add_note(["Note 2", "important,personal"], notebook)
        add_note(["Note 3", "important,work,urgent"], notebook)

        result = search_notes_by_tags(["important", "work"], notebook)
        assert "Found 2 note(s)" in result

    def test_search_by_tags_comma_separated(self):
        """Test searching with comma-separated tags."""
        notebook = NoteBook()
        add_note(["Note 1", "tag1,tag2"], notebook)
        add_note(["Note 2", "tag1"], notebook)

        result = search_notes_by_tags(["tag1,tag2"], notebook)
        assert "Found 1 note(s)" in result

    def test_search_by_tags_no_matches(self):
        """Test searching by tags with no matches."""
        notebook = NoteBook()
        add_note(["Note", "tag1"], notebook)

        result = search_notes_by_tags(["tag2"], notebook)
        assert "No notes found" in result

    def test_search_by_tags_empty_args(self):
        """Test searching with empty args."""
        notebook = NoteBook()
        result = search_notes_by_tags([], notebook)
        assert (
            "At least one tag is required" in result
            or "Enter the argument for the command" in result
        )

    def test_search_by_tags_empty_notebook(self):
        """Test searching in empty notebook."""
        notebook = NoteBook()
        result = search_notes_by_tags(["tag"], notebook)
        assert "No notes found" in result

    def test_search_by_tags_case_insensitive(self):
        """Test that tag search is case-insensitive."""
        notebook = NoteBook()
        add_note(["Note", "IMPORTANT"], notebook)

        result = search_notes_by_tags(["important"], notebook)
        assert "Found 1 note(s)" in result

    def test_search_by_tags_no_valid_tags(self):
        """Test searching with no valid tags."""
        notebook = NoteBook()
        result = search_notes_by_tags([",,"], notebook)
        assert "No valid tags provided" in result

    def test_search_by_tags_shows_tag_list(self):
        """Test that search results show searched tags."""
        notebook = NoteBook()
        add_note(["Note", "tag1,tag2"], notebook)

        result = search_notes_by_tags(["tag1", "tag2"], notebook)
        assert "tag1" in result and "tag2" in result


class TestEditNote:
    """Test suite for the edit_note handler."""

    def test_edit_note_by_number(self):
        """Test editing note by number."""
        notebook = NoteBook()
        add_note(["Original text", "tag1"], notebook)

        result = edit_note(["1", "Updated text", "tag2"], notebook)
        assert "Note updated" in result
        notes = notebook.get_all_notes()
        assert notes[0].text == "Updated text"
        assert "tag2" in notes[0].tags

    def test_edit_note_by_text_fragment(self):
        """Test editing note by text fragment."""
        notebook = NoteBook()
        add_note(["Original text"], notebook)

        result = edit_note(["Original", "Updated text"], notebook)
        assert "Note updated" in result

    def test_edit_note_text_only(self):
        """Test editing note text without tags."""
        notebook = NoteBook()
        add_note(["Original text", "tag1"], notebook)

        result = edit_note(["1", "Updated text"], notebook)
        assert "Note updated" in result
        notes = notebook.get_all_notes()
        assert notes[0].text == "Updated text"
        assert len(notes[0].tags) == 0

    def test_edit_note_with_new_tags(self):
        """Test editing note with new tags."""
        notebook = NoteBook()
        add_note(["Original text"], notebook)

        result = edit_note(["1", "Updated text", "new1,new2"], notebook)
        assert "Note updated" in result
        assert "new1" in result or "new2" in result

    def test_edit_note_not_found_by_number(self):
        """Test editing non-existent note by number."""
        notebook = NoteBook()
        result = edit_note(["99", "New text"], notebook)
        assert "not found" in result

    def test_edit_note_not_found_by_text(self):
        """Test editing non-existent note by text."""
        notebook = NoteBook()
        result = edit_note(["nonexistent", "New text"], notebook)
        assert "not found" in result

    def test_edit_note_insufficient_args(self):
        """Test editing with insufficient arguments."""
        notebook = NoteBook()
        result = edit_note(["1"], notebook)
        assert (
            "Identifier and new text are required" in result
            or "Enter the argument for the command" in result
        )

    def test_edit_note_empty_args(self):
        """Test editing with empty args."""
        notebook = NoteBook()
        result = edit_note([], notebook)
        assert (
            "Identifier and new text are required" in result
            or "Enter the argument for the command" in result
        )

    def test_edit_note_updates_timestamp(self):
        """Test that editing updates the timestamp."""
        notebook = NoteBook()
        add_note(["Original text"], notebook)
        notes_before = notebook.get_all_notes()
        original_time = notes_before[0].updated_at

        time.sleep(0.01)

        edit_note(["1", "Updated text"], notebook)
        notes_after = notebook.get_all_notes()
        assert notes_after[0].updated_at > original_time

    def test_edit_note_with_comma_separated_tags(self):
        """Test editing with comma-separated tags."""
        notebook = NoteBook()
        add_note(["Original text"], notebook)

        result = edit_note(["1", "Updated", "tag1,tag2,tag3"], notebook)
        assert "Note updated" in result


class TestDeleteNote:
    """Test suite for the delete_note handler."""

    def test_delete_note_by_number(self):
        """Test deleting note by number."""
        notebook = NoteBook()
        add_note(["Test note"], notebook)

        result = delete_note(["1"], notebook)
        assert "Note deleted" in result
        assert len(notebook) == 0

    def test_delete_note_by_text_fragment(self):
        """Test deleting note by text fragment."""
        notebook = NoteBook()
        add_note(["Test note to delete"], notebook)

        result = delete_note(["Test"], notebook)
        assert "Note deleted" in result
        assert len(notebook) == 0

    def test_delete_note_not_found_by_number(self):
        """Test deleting non-existent note by number."""
        notebook = NoteBook()
        result = delete_note(["99"], notebook)
        assert "not found" in result

    def test_delete_note_not_found_by_text(self):
        """Test deleting non-existent note by text."""
        notebook = NoteBook()
        result = delete_note(["nonexistent"], notebook)
        assert "not found" in result

    def test_delete_note_empty_args(self):
        """Test deleting with empty args."""
        notebook = NoteBook()
        result = delete_note([], notebook)
        assert (
            "Note identifier is required" in result
            or "Enter the argument for the command" in result
        )

    def test_delete_note_from_multiple(self):
        """Test deleting one note from multiple."""
        notebook = NoteBook()
        add_note(["Note 1"], notebook)
        add_note(["Note 2"], notebook)
        add_note(["Note 3"], notebook)

        result = delete_note(["2"], notebook)
        assert "Note deleted" in result
        assert len(notebook) == 2

    def test_delete_note_shows_truncated_text(self):
        """Test that delete confirmation shows truncated text."""
        notebook = NoteBook()
        long_text = "A" * 100
        add_note([long_text], notebook)

        result = delete_note(["1"], notebook)
        assert "Note deleted" in result
        assert "..." in result


class TestListNotes:
    """Test suite for the list_notes handler."""

    def test_list_notes_empty_notebook(self):
        """Test listing notes in empty notebook."""
        notebook = NoteBook()
        result = list_notes([], notebook)
        assert "No notes found" in result

    def test_list_notes_default_sort(self):
        """Test listing notes with default sorting."""
        notebook = NoteBook()
        add_note(["Note 1"], notebook)
        add_note(["Note 2"], notebook)
        add_note(["Note 3"], notebook)

        result = list_notes([], notebook)
        assert "All notes" in result
        assert "#1" in result
        assert "#2" in result
        assert "#3" in result

    def test_list_notes_sort_by_created(self):
        """Test listing notes sorted by creation date."""
        notebook = NoteBook()
        add_note(["First"], notebook)
        add_note(["Second"], notebook)

        result = list_notes(["created"], notebook)
        assert "by creation date" in result

    def test_list_notes_sort_by_updated(self):
        """Test listing notes sorted by update date."""
        notebook = NoteBook()
        add_note(["Note"], notebook)

        result = list_notes(["updated"], notebook)
        assert "by update date" in result

    def test_list_notes_sort_by_text(self):
        """Test listing notes sorted alphabetically."""
        notebook = NoteBook()
        add_note(["Zebra"], notebook)
        add_note(["Apple"], notebook)

        result = list_notes(["text"], notebook)
        assert "alphabetically" in result

    def test_list_notes_sort_by_tags(self):
        """Test listing notes sorted by tags."""
        notebook = NoteBook()
        add_note(["Note", "tag1"], notebook)

        result = list_notes(["tags"], notebook)
        assert "by tags" in result

    def test_list_notes_sort_equals_format(self):
        """Test listing with sort=parameter format."""
        notebook = NoteBook()
        add_note(["Note"], notebook)

        result = list_notes(["sort=text"], notebook)
        assert "All notes" in result

    def test_list_notes_invalid_sort(self):
        """Test listing with invalid sort parameter."""
        notebook = NoteBook()
        add_note(["Note"], notebook)

        result = list_notes(["invalid"], notebook)
        assert "All notes" in result

    def test_list_notes_shows_all_note_info(self):
        """Test that listing shows note text and tags."""
        notebook = NoteBook()
        add_note(["Test note", "tag1,tag2"], notebook)

        result = list_notes([], notebook)
        assert "Test note" in result
        assert "Tags:" in result


class TestIntegrationNoteHandlers:
    """Integration tests for note handlers."""

    def test_full_workflow(self):
        """Test complete workflow with all operations."""
        notebook = NoteBook()

        # Add notes
        add_note(["Buy groceries", "shopping,important"], notebook)
        add_note(["Call dentist", "health,urgent"], notebook)
        add_note(["Finish report", "work,important"], notebook)

        assert len(notebook) == 3

        # Search
        result = search_notes(["important"], notebook)
        assert "Found 2 note(s)" in result

        # Search by tags
        result = search_notes_by_tags(["shopping"], notebook)
        assert "Found 1 note(s)" in result

        # Edit note
        edit_note(["1", "Buy groceries and snacks", "shopping"], notebook)

        # List all
        result = list_notes([], notebook)
        assert "All notes" in result

        # Delete
        delete_note(["2"], notebook)
        assert len(notebook) == 2

    def test_edge_cases_combination(self):
        """Test combination of edge cases."""
        notebook = NoteBook()

        # Add note with many tags
        add_note(["Important", "tag1,tag2,tag3,tag4,tag5"], notebook)

        # Edit with different tags
        edit_note(["1", "Very important", "newtag1,newtag2"], notebook)

        # Search by old tags should fail
        result = search_notes_by_tags(["tag1"], notebook)
        assert "No notes found" in result

        # Search by new tags should succeed
        result = search_notes_by_tags(["newtag1"], notebook)
        assert "Found 1 note(s)" in result

    def test_error_handling_sequence(self):
        """Test error handling in sequence of operations."""
        notebook = NoteBook()

        # Try to search in empty notebook
        result = search_notes(["anything"], notebook)
        assert "No notes found" in result

        # Try to delete non-existent note
        result = delete_note(["1"], notebook)
        assert "not found" in result

        # Try to edit non-existent note
        result = edit_note(["1", "new text"], notebook)
        assert "not found" in result

        # Add a note
        add_note(["Test"], notebook)

        # Now operations should work
        result = search_notes(["Test"], notebook)
        assert "Found 1 note(s)" in result


class TestAddEmail:
    """Test suite for the add_email handler."""

    def test_add_email_to_existing_contact(self):
        """Test adding email to existing contact."""
        book = AddressBook()
        record = Record("John Doe")
        book.add_record(record)
        result = add_email(["John Doe", "test@example.com"], book)
        assert "added" in result.lower() or "updated" in result.lower()
        assert record.email is not None
        assert record.email.value == "test@example.com"

    def test_update_email_to_existing_contact(self):
        """Test updating email for existing contact."""
        book = AddressBook()
        record = Record("John Doe")
        record.add_email("old@example.com")
        book.add_record(record)
        result = add_email(["John Doe", "new@example.com"], book)
        assert "updated" in result.lower() or "added" in result.lower()
        assert record.email.value == "new@example.com"

    def test_add_email_to_nonexistent_contact(self):
        """Test adding email to non-existent contact."""
        book = AddressBook()
        result = add_email(["Nonexistent", "test@example.com"], book)
        assert "not found" in result.lower()

    def test_add_email_missing_args(self):
        """Test adding email with missing arguments."""
        book = AddressBook()
        result = add_email(["John"], book)
        assert "Error" in result and "requires" in result.lower()

    def test_add_email_invalid_format(self):
        """Test adding email with invalid format."""
        book = AddressBook()
        record = Record("John Doe")
        book.add_record(record)
        result = add_email(["John Doe", "invalid-email"], book)
        assert "Error" in result or "Invalid email format" in result


class TestDeleteEmail:
    """Test suite for the delete_email handler."""

    def test_delete_email(self):
        """Test deleting email from contact."""
        book = AddressBook()
        record = Record("John Doe")
        record.add_email("test@example.com")
        book.add_record(record)
        result = delete_email(["John Doe"], book)
        assert "deleted" in result.lower()
        assert record.email is None

    def test_delete_email_no_email(self):
        """Test deleting email when contact has no email."""
        book = AddressBook()
        record = Record("John Doe")
        book.add_record(record)
        result = delete_email(["John Doe"], book)
        assert "no email" in result.lower()

    def test_delete_email_not_found(self):
        """Test deleting email for non-existent contact."""
        book = AddressBook()
        result = delete_email(["Nonexistent"], book)
        assert "not found" in result.lower()

    def test_delete_email_missing_args(self):
        """Test deleting email with missing arguments."""
        book = AddressBook()
        result = delete_email([], book)
        assert "Error" in result and "requires" in result.lower()


class TestShowEmail:
    """Test suite for the show_email handler."""

    def test_show_email_with_email(self):
        """Test showing contact with email."""
        book = AddressBook()
        record = Record("John Doe")
        record.add_email("test@example.com")
        book.add_record(record)
        result = show_email(["John Doe"], book)
        assert "test@example.com" in result

    def test_show_email_no_email(self):
        """Test showing contact without email."""
        book = AddressBook()
        record = Record("John Doe")
        book.add_record(record)
        result = show_email(["John Doe"], book)
        assert "no email" in result.lower()

    def test_show_email_not_found(self):
        """Test showing email for non-existent contact."""
        book = AddressBook()
        result = show_email(["Nonexistent"], book)
        assert "not found" in result.lower()

    def test_show_email_missing_args(self):
        """Test showing email with missing arguments."""
        book = AddressBook()
        result = show_email([], book)
        assert "Error" in result and "requires" in result.lower()
