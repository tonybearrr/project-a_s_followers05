"""
Tests for the Field class.

This module contains tests for the base Field class functionality.
"""

from models.field import Field


class TestField:
    """Test suite for the Field class."""

    def test_init_with_string_value(self):
        """Test Field initialization with a string value."""
        field = Field("test value")
        assert field.value == "test value"

    def test_init_with_integer_value(self):
        """Test Field initialization with an integer value."""
        field = Field(123)
        assert field.value == 123

    def test_init_with_none_value(self):
        """Test Field initialization with None value."""
        field = Field(None)
        assert field.value is None

    def test_init_with_empty_string(self):
        """Test Field initialization with empty string."""
        field = Field("")
        assert field.value == ""

    def test_str_representation_string(self):
        """Test string representation returns correct string."""
        field = Field("Hello World")
        assert str(field) == "Hello World"

    def test_str_representation_integer(self):
        """Test string representation of integer value."""
        field = Field(42)
        assert str(field) == "42"

    def test_str_representation_none(self):
        """Test string representation of None value."""
        field = Field(None)
        assert str(field) == "None"

    def test_value_modification(self):
        """Test that Field value can be modified."""
        field = Field("original")
        field.value = "modified"
        assert field.value == "modified"

    def test_multiple_field_instances(self):
        """Test that multiple Field instances are independent."""
        field1 = Field("value1")
        field2 = Field("value2")

        assert field1.value == "value1"
        assert field2.value == "value2"
        assert field1.value != field2.value
