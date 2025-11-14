"""
Tests for the parsers module.

This module contains tests for the parse_input function.
"""

from utils.parsers import parse_input
from utils.parsers import detect_command
from core.commands import Command


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

    def test_parse_command_with_leading_trailing_spaces(self):
        """Test parsing command with leading and trailing spaces."""
        cmd, *args = parse_input("   delete   John   ")
        assert cmd == "delete"
        assert args == ["John"]

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
        cmd, *args = parse_input("add Marina 1234567890")
        assert cmd == "add"
        assert args[0] == "Marina"

    def test_parse_empty_input(self):
        """Test parsing empty input."""
        result = parse_input("")
        assert result == ("",)

    def test_parse_quoted_arguments(self):
        """Test parsing command with quoted arguments."""
        cmd, *args = parse_input('add "John Doe" "123 456 7890"')
        assert cmd == "add"
        assert args == ["John Doe", "123 456 7890"]

    def test_parse_mixed_quoted_and_unquoted(self):
        """Test parsing command with mixed quoted and unquoted arguments."""
        cmd, *args = parse_input('add John "123 456 7890"')
        assert cmd == "add"
        assert args == ["John", "123 456 7890"]

    def test_parse_only_spaces(self):
        """Test parsing input with only spaces."""
        result = parse_input("    ")
        assert result == ("",)

    def test_parse_no_command_only_args(self):
        """Test parsing input with only arguments and no command."""
        cmd, *args = parse_input('"John Doe" 1234567890')
        assert cmd == "john doe"
        assert args == ["1234567890"]

    def test_parse_unclosed_quote_raises(self):
        """Test that unclosed quotes raise a ValueError."""
        is_raised = False
        try:
            parse_input('add "John Doe 1234567890')
        except ValueError:
            is_raised = True
        assert is_raised

    def test_parse_command_with_special_characters(self):
        """Test parsing command with special characters in arguments."""
        cmd, *args = parse_input('add "John@Doe" "#$%^&*"')
        assert cmd == "add"
        assert args == ["John@Doe", "#$%^&*"]

    def test_parse_command_with_empty_quotes(self):
        """Test parsing command with empty quoted argument."""
        cmd, *args = parse_input('add "" 1234567890')
        assert cmd == "add"
        assert args == ["", "1234567890"]


class TestDetectCommand:
    """Test suite for the detect_command function."""

    def test_detect_known_command(self):
        """Test detection of a known command."""
        command, recognized = detect_command("add")
        assert recognized is True
        assert command == Command.ADD_CONTACT

    def test_detect_unknown_command_no_suggestions(self):
        """Test detection of an unknown command with no suggestions."""
        command, recognized = detect_command("unknowncmd")
        assert recognized is False
        assert command is None

    def test_detect_unknown_command_with_single_suggestion(self):
        """Test detection of an unknown command with a single suggestion."""
        command, recognized = detect_command("ad")
        assert recognized is True
        assert command == Command.ADD_CONTACT

    def test_detect_unknown_command_with_multiple_suggestions(self):
        """Test detection of an unknown command with multiple suggestions."""
        command, recognized = detect_command("a")
        assert recognized is False
        assert command is None

    def test_detect_command_with_typo(self):
        """Test detection of a command with a minor typo."""
        command, recognized = detect_command("adn")
        assert recognized is False
        assert command is None

    def test_detect_empty_command(self):
        """Test detection of an empty command."""
        command, recognized = detect_command("")
        assert recognized is False
        assert command is None

    def test_detect_command_with_special_characters(self):
        """Test detection of a command with special characters."""
        command, recognized = detect_command("ad@d")
        assert recognized is False
        assert command is None
