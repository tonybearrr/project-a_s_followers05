"""
Tests for the main module.

This module contains tests for the main functionality and get_output_by_command.
"""

from main import get_output_by_command
from core.commands import Command
from models.address_book import AddressBook
from models.notebook import NoteBook


class TestGetOutputByCommand:
    """Test suite for the get_output_by_command function."""

    def test_exit_command_exit_1(self):
        """Test exit command with EXIT_1."""
        book = AddressBook()
        notebook = NoteBook()
        output, is_exit = get_output_by_command(Command.EXIT_1, [], book, notebook)
        assert is_exit is True
        assert output == "Good bye!"

    def test_exit_command_exit_2(self):
        """Test exit command with EXIT_2."""
        book = AddressBook()
        notebook = NoteBook()
        output, is_exit = get_output_by_command(Command.EXIT_2, [], book, notebook)
        assert is_exit is True
        assert output == "Good bye!"

    def test_hello_command(self):
        """Test hello command."""
        book = AddressBook()
        notebook = NoteBook()
        output, is_exit = get_output_by_command(Command.HELLO, [], book, notebook)
        assert is_exit is False
        assert output == "How can I help you?"

    def test_add_contact_command(self):
        """Test add contact command."""
        book = AddressBook()
        notebook = NoteBook()
        output, is_exit = get_output_by_command(Command.ADD_CONTACT, ["John", "1234567890"], book, notebook)
        assert is_exit is False
        assert "added successfully" in output.lower() or "updated successfully" in output.lower()

    def test_show_all_contacts_command(self):
        """Test show all contacts command."""
        book = AddressBook()
        notebook = NoteBook()
        output, is_exit = get_output_by_command(Command.SHOW_ALL_CONTACTS, [], book, notebook)
        assert is_exit is False
        assert "No contacts found" in output or "Contact name" in output

    def test_unknown_command(self):
        """Test unknown command."""
        book = AddressBook()
        notebook = NoteBook()
        output, is_exit = get_output_by_command("unknown_command", [], book, notebook)
        assert is_exit is False
        assert output == "Unknown command. Please try again."

    def test_help_command(self):
        """Test help command."""
        book = AddressBook()
        notebook = NoteBook()
        output, is_exit = get_output_by_command(Command.HELP, [], book, notebook)
        assert is_exit is False
        assert "Available commands" in output
        assert Command.HELLO in output
        assert Command.ADD_CONTACT in output

    def test_help_alt_command(self):
        """Test help alternative command."""
        book = AddressBook()
        notebook = NoteBook()
        output, is_exit = get_output_by_command(Command.HELP_ALT, [], book, notebook)
        assert is_exit is False
        assert "Available commands" in output


class TestNoteCommands:
    """Test suite for note commands in main."""

    def test_add_note_command_valid(self):
        """Test add-note command with valid data."""
        book = AddressBook()
        notebook = NoteBook()
        output, is_exit = get_output_by_command(Command.ADD_NOTE, ["Test note", "tag1"], book, notebook)
        assert is_exit is False
        assert "Note #1 added" in output
        assert len(notebook) == 1

    def test_add_note_command_no_args(self):
        """Test add-note command without arguments."""
        book = AddressBook()
        notebook = NoteBook()
        output, is_exit = get_output_by_command(Command.ADD_NOTE, [], book, notebook)
        assert is_exit is False
        assert "required" in output.lower() or "argument" in output.lower()

    def test_add_note_command_empty_text(self):
        """Test add-note command with empty text."""
        book = AddressBook()
        notebook = NoteBook()
        output, is_exit = get_output_by_command(Command.ADD_NOTE, [""], book, notebook)
        assert is_exit is False
        assert "empty" in output.lower() or "required" in output.lower()

    def test_add_note_command_with_multiple_tags(self):
        """Test add-note command with multiple tags."""
        book = AddressBook()
        notebook = NoteBook()
        output, is_exit = get_output_by_command(
            Command.ADD_NOTE,
            ["Important note", "urgent,work,priority"],
            book,
            notebook
        )
        assert is_exit is False
        assert "Note #1 added" in output

    def test_list_notes_command_empty(self):
        """Test list-notes command with empty notebook."""
        book = AddressBook()
        notebook = NoteBook()
        output, is_exit = get_output_by_command(Command.LIST_NOTES, [], book, notebook)
        assert is_exit is False
        assert "No notes found" in output

    def test_list_notes_command_with_notes(self):
        """Test list-notes command with existing notes."""
        book = AddressBook()
        notebook = NoteBook()
        get_output_by_command(Command.ADD_NOTE, ["Note 1"], book, notebook)
        get_output_by_command(Command.ADD_NOTE, ["Note 2"], book, notebook)

        output, is_exit = get_output_by_command(Command.LIST_NOTES, [], book, notebook)
        assert is_exit is False
        assert "All notes" in output
        assert "#1" in output
        assert "#2" in output

    def test_list_notes_command_with_sort(self):
        """Test list-notes command with sorting parameter."""
        book = AddressBook()
        notebook = NoteBook()
        get_output_by_command(Command.ADD_NOTE, ["Zebra"], book, notebook)
        get_output_by_command(Command.ADD_NOTE, ["Apple"], book, notebook)

        output, is_exit = get_output_by_command(Command.LIST_NOTES, ["text"], book, notebook)
        assert is_exit is False
        assert "alphabetically" in output

    def test_list_notes_command_invalid_sort(self):
        """Test list-notes command with invalid sort parameter."""
        book = AddressBook()
        notebook = NoteBook()
        get_output_by_command(Command.ADD_NOTE, ["Note"], book, notebook)

        output, is_exit = get_output_by_command(Command.LIST_NOTES, ["invalid"], book, notebook)
        assert is_exit is False
        assert "All notes" in output

    def test_search_notes_command_found(self):
        """Test search-notes command with results."""
        book = AddressBook()
        notebook = NoteBook()
        get_output_by_command(Command.ADD_NOTE, ["Buy groceries"], book, notebook)
        get_output_by_command(Command.ADD_NOTE, ["Buy tickets"], book, notebook)
        get_output_by_command(Command.ADD_NOTE, ["Call mom"], book, notebook)

        output, is_exit = get_output_by_command(Command.SEARCH_NOTES, ["buy"], book, notebook)
        assert is_exit is False
        assert "Found 2 note(s)" in output

    def test_search_notes_command_not_found(self):
        """Test search-notes command with no results."""
        book = AddressBook()
        notebook = NoteBook()
        get_output_by_command(Command.ADD_NOTE, ["Test note"], book, notebook)

        output, is_exit = get_output_by_command(Command.SEARCH_NOTES, ["nonexistent"], book, notebook)
        assert is_exit is False
        assert "No notes found" in output

    def test_search_notes_command_empty_query(self):
        """Test search-notes command without query."""
        book = AddressBook()
        notebook = NoteBook()
        output, is_exit = get_output_by_command(Command.SEARCH_NOTES, [], book, notebook)
        assert is_exit is False
        assert "required" in output.lower() or "argument" in output.lower()

    def test_search_notes_command_empty_notebook(self):
        """Test search-notes command in empty notebook."""
        book = AddressBook()
        notebook = NoteBook()
        output, is_exit = get_output_by_command(Command.SEARCH_NOTES, ["anything"], book, notebook)
        assert is_exit is False
        assert "No notes found" in output

    def test_search_tags_command_found(self):
        """Test search-tags command with results."""
        book = AddressBook()
        notebook = NoteBook()
        get_output_by_command(Command.ADD_NOTE, ["Note 1", "important"], book, notebook)
        get_output_by_command(Command.ADD_NOTE, ["Note 2", "urgent"], book, notebook)
        get_output_by_command(Command.ADD_NOTE, ["Note 3", "important"], book, notebook)

        output, is_exit = get_output_by_command(Command.SEARCH_TAGS, ["important"], book, notebook)
        assert is_exit is False
        assert "Found 2 note(s)" in output

    def test_search_tags_command_multiple_tags(self):
        """Test search-tags command with multiple tags."""
        book = AddressBook()
        notebook = NoteBook()
        get_output_by_command(Command.ADD_NOTE, ["Note 1", "important,work"], book, notebook)
        get_output_by_command(Command.ADD_NOTE, ["Note 2", "important"], book, notebook)

        output, is_exit = get_output_by_command(Command.SEARCH_TAGS, ["important,work"], book, notebook)
        assert is_exit is False
        assert "Found 1 note(s)" in output

    def test_search_tags_command_not_found(self):
        """Test search-tags command with no results."""
        book = AddressBook()
        notebook = NoteBook()
        get_output_by_command(Command.ADD_NOTE, ["Note", "tag1"], book, notebook)

        output, is_exit = get_output_by_command(Command.SEARCH_TAGS, ["tag2"], book, notebook)
        assert is_exit is False
        assert "No notes found" in output

    def test_search_tags_command_empty_args(self):
        """Test search-tags command without arguments."""
        book = AddressBook()
        notebook = NoteBook()
        output, is_exit = get_output_by_command(Command.SEARCH_TAGS, [], book, notebook)
        assert is_exit is False
        assert "required" in output.lower() or "argument" in output.lower()

    def test_search_tags_command_no_valid_tags(self):
        """Test search-tags command with only invalid tags."""
        book = AddressBook()
        notebook = NoteBook()
        output, is_exit = get_output_by_command(Command.SEARCH_TAGS, [",,"], book, notebook)
        assert is_exit is False
        assert "No valid tags" in output

    def test_edit_note_command_by_number(self):
        """Test edit-note command by note number."""
        book = AddressBook()
        notebook = NoteBook()
        get_output_by_command(Command.ADD_NOTE, ["Original", "tag1"], book, notebook)

        output, is_exit = get_output_by_command(
            Command.EDIT_NOTE,
            ["1", "Updated", "tag2"],
            book,
            notebook
        )
        assert is_exit is False
        assert "Note updated" in output

    def test_edit_note_command_by_text(self):
        """Test edit-note command by text fragment."""
        book = AddressBook()
        notebook = NoteBook()
        get_output_by_command(Command.ADD_NOTE, ["Original text"], book, notebook)

        output, is_exit = get_output_by_command(
            Command.EDIT_NOTE,
            ["Original", "Updated text"],
            book,
            notebook
        )
        assert is_exit is False
        assert "Note updated" in output

    def test_edit_note_command_not_found(self):
        """Test edit-note command with non-existent note."""
        book = AddressBook()
        notebook = NoteBook()
        output, is_exit = get_output_by_command(
            Command.EDIT_NOTE,
            ["99", "New text"],
            book,
            notebook
        )
        assert is_exit is False
        assert "not found" in output.lower()

    def test_edit_note_command_insufficient_args(self):
        """Test edit-note command without enough arguments."""
        book = AddressBook()
        notebook = NoteBook()
        output, is_exit = get_output_by_command(Command.EDIT_NOTE, ["1"], book, notebook)
        assert is_exit is False
        assert "required" in output.lower() or "argument" in output.lower()

    def test_edit_note_command_empty_args(self):
        """Test edit-note command without arguments."""
        book = AddressBook()
        notebook = NoteBook()
        output, is_exit = get_output_by_command(Command.EDIT_NOTE, [], book, notebook)
        assert is_exit is False
        assert "required" in output.lower() or "argument" in output.lower()

    def test_edit_note_command_with_new_tags(self):
        """Test edit-note command with new tags."""
        book = AddressBook()
        notebook = NoteBook()
        get_output_by_command(Command.ADD_NOTE, ["Note"], book, notebook)

        output, is_exit = get_output_by_command(
            Command.EDIT_NOTE,
            ["1", "Updated", "new1,new2,new3"],
            book,
            notebook
        )
        assert is_exit is False
        assert "Note updated" in output

    def test_delete_note_command_by_number(self):
        """Test delete-note command by number."""
        book = AddressBook()
        notebook = NoteBook()
        get_output_by_command(Command.ADD_NOTE, ["Test note"], book, notebook)

        output, is_exit = get_output_by_command(Command.DELETE_NOTE, ["1"], book, notebook)
        assert is_exit is False
        assert "Note deleted" in output
        assert len(notebook) == 0

    def test_delete_note_command_by_text(self):
        """Test delete-note command by text fragment."""
        book = AddressBook()
        notebook = NoteBook()
        get_output_by_command(Command.ADD_NOTE, ["Delete this note"], book, notebook)

        output, is_exit = get_output_by_command(Command.DELETE_NOTE, ["Delete"], book, notebook)
        assert is_exit is False
        assert "Note deleted" in output

    def test_delete_note_command_not_found(self):
        """Test delete-note command with non-existent note."""
        book = AddressBook()
        notebook = NoteBook()
        output, is_exit = get_output_by_command(Command.DELETE_NOTE, ["99"], book, notebook)
        assert is_exit is False
        assert "not found" in output.lower()

    def test_delete_note_command_empty_args(self):
        """Test delete-note command without arguments."""
        book = AddressBook()
        notebook = NoteBook()
        output, is_exit = get_output_by_command(Command.DELETE_NOTE, [], book, notebook)
        assert is_exit is False
        assert "required" in output.lower() or "argument" in output.lower()

    def test_delete_note_command_from_multiple(self):
        """Test deleting one note from multiple."""
        book = AddressBook()
        notebook = NoteBook()
        get_output_by_command(Command.ADD_NOTE, ["Note 1"], book, notebook)
        get_output_by_command(Command.ADD_NOTE, ["Note 2"], book, notebook)
        get_output_by_command(Command.ADD_NOTE, ["Note 3"], book, notebook)

        output, is_exit = get_output_by_command(Command.DELETE_NOTE, ["2"], book, notebook)
        assert is_exit is False
        assert "Note deleted" in output
        assert len(notebook) == 2


# ... existing code ...

class TestNoteCommandsIntegration:
    """Integration tests for note commands workflow."""

    def test_complete_note_workflow(self):
        """Test complete workflow with all note commands."""
        book = AddressBook()
        notebook = NoteBook()

        # Add notes
        output, _ = get_output_by_command(
            Command.ADD_NOTE,
            ["Buy groceries", "shopping,important"],
            book,
            notebook
        )
        assert "added" in output.lower()
        assert len(notebook) == 1

        output, _ = get_output_by_command(
            Command.ADD_NOTE,
            ["Call dentist", "health"],
            book,
            notebook
        )
        assert "added" in output.lower()
        assert len(notebook) == 2

        # List notes
        output, _ = get_output_by_command(Command.LIST_NOTES, [], book, notebook)
        assert "All notes" in output
        assert len(notebook) == 2

        # Search notes
        output, _ = get_output_by_command(Command.SEARCH_NOTES, ["buy"], book, notebook)
        assert "Found 1 note(s)" in output

        # Search by tags
        output, _ = get_output_by_command(Command.SEARCH_TAGS, ["shopping"], book, notebook)
        assert "Found 1 note(s)" in output

        # Edit note
        output, _ = get_output_by_command(
            Command.EDIT_NOTE,
            ["1", "Buy groceries and milk", "shopping"],
            book,
            notebook
        )
        assert "Note updated" in output

        # Delete note
        output, _ = get_output_by_command(Command.DELETE_NOTE, ["2"], book, notebook)
        assert "Note deleted" in output
        assert len(notebook) == 1

    def test_note_commands_with_special_characters(self):
        """Test note commands with special characters."""
        book = AddressBook()
        notebook = NoteBook()

        # Unicode text
        output, _ = get_output_by_command(
            Command.ADD_NOTE,
            ["Нотатка українською 🎉", "тег"],
            book,
            notebook
        )
        assert "added" in output.lower()

        # Search with special chars
        output, _ = get_output_by_command(Command.SEARCH_NOTES, ["українською"], book, notebook)
        assert "Found 1 note(s)" in output

        # Search tags with unicode
        output, _ = get_output_by_command(Command.SEARCH_TAGS, ["тег"], book, notebook)
        assert "Found 1 note(s)" in output

    def test_note_commands_with_very_long_text(self):
        """Test note commands with very long text."""
        book = AddressBook()
        notebook = NoteBook()

        long_text = "A" * 1000
        output, _ = get_output_by_command(Command.ADD_NOTE, [long_text], book, notebook)
        assert "added" in output.lower()

        # Delete should show truncated text
        output, _ = get_output_by_command(Command.DELETE_NOTE, ["1"], book, notebook)
        assert "Note deleted" in output
        assert "..." in output

    def test_note_commands_error_sequence(self):
        """Test error handling in sequence of operations."""
        book = AddressBook()
        notebook = NoteBook()

        # Try operations on empty notebook
        output, _ = get_output_by_command(Command.SEARCH_NOTES, ["test"], book, notebook)
        assert "No notes found" in output

        output, _ = get_output_by_command(Command.DELETE_NOTE, ["1"], book, notebook)
        assert "not found" in output.lower()

        output, _ = get_output_by_command(Command.EDIT_NOTE, ["1", "text"], book, notebook)
        assert "not found" in output.lower()

        # Add note and verify operations work
        get_output_by_command(Command.ADD_NOTE, ["Test"], book, notebook)

        output, _ = get_output_by_command(Command.SEARCH_NOTES, ["test"], book, notebook)
        assert "Found 1 note(s)" in output

    def test_note_commands_with_many_tags(self):
        """Test note commands with many tags."""
        book = AddressBook()
        notebook = NoteBook()

        many_tags = ",".join([f"tag{i}" for i in range(20)])
        output, _ = get_output_by_command(
            Command.ADD_NOTE,
            ["Note with many tags", many_tags],
            book,
            notebook
        )
        assert "added" in output.lower()

        # Search should find it
        output, _ = get_output_by_command(Command.SEARCH_TAGS, ["tag5"], book, notebook)
        assert "Found 1 note(s)" in output

    def test_note_commands_case_insensitivity(self):
        """Test case insensitivity in note operations."""
        book = AddressBook()
        notebook = NoteBook()

        get_output_by_command(Command.ADD_NOTE, ["IMPORTANT NOTE", "URGENT"], book, notebook)

        # Search text (case insensitive)
        output, _ = get_output_by_command(Command.SEARCH_NOTES, ["important"], book, notebook)
        assert "Found 1 note(s)" in output

        # Search tags (case insensitive)
        output, _ = get_output_by_command(Command.SEARCH_TAGS, ["urgent"], book, notebook)
        assert "Found 1 note(s)" in output

    def test_note_sorting_options(self):
        """Test all sorting options for list-notes."""
        book = AddressBook()
        notebook = NoteBook()

        get_output_by_command(Command.ADD_NOTE, ["Zebra", "z-tag"], book, notebook)
        get_output_by_command(Command.ADD_NOTE, ["Apple", "a-tag"], book, notebook)

        # Sort by text
        output, _ = get_output_by_command(Command.LIST_NOTES, ["text"], book, notebook)
        assert "alphabetically" in output

        # Sort by tags
        output, _ = get_output_by_command(Command.LIST_NOTES, ["tags"], book, notebook)
        assert "by tags" in output

        # Sort by created
        output, _ = get_output_by_command(Command.LIST_NOTES, ["created"], book, notebook)
        assert "by creation date" in output

        # Sort by updated
        output, _ = get_output_by_command(Command.LIST_NOTES, ["updated"], book, notebook)
        assert "by update date" in output
