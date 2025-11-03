"""
Tests for the parsers module.

This module contains tests for the parse_input function.
"""

from utils.parsers import parse_input


class TestParseInput:
    """Test suite for the parse_input function."""

    def test_parse_simple_command(self):
        """Test parsing a simple command."""
        cmd, *args = parse_input("hello")
        assert cmd == "hello"
        assert not args

    def test_parse_command_with_args(self):
        """Test parsing a command with arguments."""
        cmd, *args = parse_input("add John 1234567890")
        assert cmd == "add"
        assert args == ["John", "1234567890"]

    def test_parse_command_lowercase(self):
        """Test that command is converted to lowercase."""
        cmd, *_ = parse_input("HELLO")
        assert cmd == "hello"

    def test_parse_command_with_multiple_args(self):
        """Test parsing command with multiple arguments."""
        cmd, *args = parse_input("change John 1234567890 9876543210")
        assert cmd == "change"
        assert len(args) == 3

    def test_parse_command_with_spaces(self):
        """Test parsing command with extra spaces."""
        cmd, *args = parse_input("  add   John  Doe   1234567890  ")
        assert cmd == "add"
        assert len(args) >= 2

    def test_parse_command_with_tabs(self):
        """Test parsing command with tab separators."""
        cmd, *args = parse_input("add\tJohn\t1234567890")
        assert cmd == "add"
        assert args == ["John", "1234567890"]

    def test_parse_unicode_command(self):
        """Test parsing command with unicode characters."""
        cmd, *args = parse_input("add Степан 1234567890")
        assert cmd == "add"
        assert args[0] == "Степан"

    def test_parse_empty_input(self):
        """Test parsing empty input."""
        result = parse_input("")
        assert result == ("",)

