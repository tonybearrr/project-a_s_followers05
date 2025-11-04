"""
Tests for the Phone class.

This module contains tests for the Phone field validation functionality.
"""

from models.phone import Phone


class TestPhone:
    """Test suite for the Phone class."""

    def test_init_with_valid_10_digit_phone(self):
        """Test Phone initialization with valid 10-digit number."""
        phone = Phone("1234567890")
        assert phone.value == "1234567890"

    def test_init_with_formatted_phone(self):
        """Test Phone initialization with formatted number (spaces, dashes)."""
        phone = Phone("123-456-7890")
        assert phone.value == "1234567890"

        phone = Phone("123 456 7890")
        assert phone.value == "1234567890"

        phone = Phone("(123) 456-7890")
        assert phone.value == "1234567890"

    def test_str_representation(self):
        """Test string representation of Phone."""
        phone = Phone("1234567890")
        assert str(phone) == "1234567890"

    def test_value_attribute_access(self):
        """Test accessing the value attribute."""
        phone = Phone("9876543210")
        assert phone.value == "9876543210"

    def test_raises_error_on_wrong_length(self):
        """Test that Phone raises ValueError for wrong length."""
        for invalid_phone in ["123", "12345", "12345678901234"]:
            try:
                Phone(invalid_phone)
                assert False, f"Expected ValueError for phone: {invalid_phone}"
            except ValueError as e:
                error_msg = str(e)
                assert "Phone number must be 10 digits" in error_msg or "Phone number cannot be empty" in error_msg

    def test_raises_error_on_non_numeric_characters(self):
        """Test that Phone raises ValueError for non-numeric characters after cleaning."""
        # These should fail because after cleaning, they don't have 10 digits
        for invalid_phone in ["123456789a", "abcdefghij", "12345-6789", "123 456 789"]:
            try:
                Phone(invalid_phone)
                assert False, f"Expected ValueError for phone: {invalid_phone}"
            except ValueError as e:
                error_msg = str(e)
                assert "Phone number must be 10 digits" in error_msg or "Phone number cannot be empty" in error_msg

    def test_raises_error_on_empty_string(self):
        """Test that Phone raises ValueError for empty string."""
        try:
            Phone("")
            assert False, "Expected ValueError for empty string"
        except ValueError as e:
            assert "Phone number cannot be empty" in str(e)

    def test_raises_error_on_none(self):
        """Test that Phone raises error for None."""
        try:
            Phone(None)
            assert False, "Expected error for None"
        except (ValueError, AttributeError, TypeError):
            pass  # Expected either ValueError, AttributeError, or TypeError
