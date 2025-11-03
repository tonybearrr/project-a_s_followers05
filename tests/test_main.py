"""
Tests for the main module.

This module contains tests for the main functionality and get_output_by_command.
"""

from main import get_output_by_command
from core.commands import Command
from models.AddressBook import AddressBook


class TestGetOutputByCommand:
    """Test suite for the get_output_by_command function."""

    def test_exit_command_exit_1(self):
        """Test exit command with EXIT_1."""
        book = AddressBook()
        output, is_exit = get_output_by_command(Command.EXIT_1, [], book)
        assert is_exit is True
        assert output == "Good bye!"

    def test_exit_command_exit_2(self):
        """Test exit command with EXIT_2."""
        book = AddressBook()
        output, is_exit = get_output_by_command(Command.EXIT_2, [], book)
        assert is_exit is True
        assert output == "Good bye!"

    def test_hello_command(self):
        """Test hello command."""
        book = AddressBook()
        output, is_exit = get_output_by_command(Command.HELLO, [], book)
        assert is_exit is False
        assert output == "How can I help you?"

    def test_add_contact_command(self):
        """Test add contact command."""
        book = AddressBook()
        output, is_exit = get_output_by_command(Command.ADD_CONTACT, ["John", "1234567890"], book)
        assert is_exit is False
        assert "added successfully" in output.lower() or "updated successfully" in output.lower()

    def test_show_all_contacts_command(self):
        """Test show all contacts command."""
        book = AddressBook()
        output, is_exit = get_output_by_command(Command.SHOW_ALL_CONTACTS, [], book)
        assert is_exit is False
        assert "No contacts found" in output or "Contact name" in output

    def test_unknown_command(self):
        """Test unknown command."""
        book = AddressBook()
        output, is_exit = get_output_by_command("unknown_command", [], book)
        assert is_exit is False
        assert output == "Unknown command. Please try again."

    def test_help_command(self):
        """Test help command."""
        book = AddressBook()
        output, is_exit = get_output_by_command(Command.HELP, [], book)
        assert is_exit is False
        assert "Available commands" in output
        assert Command.HELLO in output
        assert Command.ADD_CONTACT in output

    def test_help_alt_command(self):
        """Test help alternative command."""
        book = AddressBook()
        output, is_exit = get_output_by_command(Command.HELP_ALT, [], book)
        assert is_exit is False
        assert "Available commands" in output
