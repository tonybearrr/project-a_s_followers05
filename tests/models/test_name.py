"""
Tests for the Name class.

This module contains tests for the Name field validation functionality.
"""

from models.Name import Name


class TestName:
    """Test suite for the Name class."""

    def test_init_with_valid_name(self):
        """Test Name initialization with a valid name."""
        name = Name("John Doe")
        assert name.value == "John Doe"

    def test_init_with_single_word_name(self):
        """Test Name initialization with a single word."""
        name = Name("John")
        assert name.value == "John"

    def test_init_raises_error_on_empty_string(self):
        """Test that Name raises ValueError for empty string."""
        try:
            Name("")
            assert False, "Expected ValueError for empty string"
        except ValueError as e:
            assert str(e) == "Name cannot be empty"

    def test_init_raises_error_on_none(self):
        """Test that Name raises ValueError for None."""
        try:
            Name(None)
            assert False, "Expected ValueError for None"
        except ValueError as e:
            assert str(e) == "Name cannot be empty"

    def test_str_representation(self):
        """Test string representation of Name."""
        name = Name("Jane Smith")
        assert str(name) == "Jane Smith"

    def test_value_attribute_access(self):
        """Test accessing the value attribute."""
        name = Name("Test User")
        assert name.value == "Test User"

    def test_name_with_unicode_characters(self):
        """Test Name with Unicode characters."""
        name = Name("Степан Бандера")
        assert name.value == "Степан Бандера"
