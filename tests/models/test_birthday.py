"""
Tests for the Birthday class.

This module contains tests for the Birthday field validation functionality.
"""

from datetime import date
from models.birthday import Birthday


class TestBirthday:
    """Test suite for the Birthday class."""

    def test_init_with_valid_date(self):
        """Test Birthday initialization with valid date format."""
        birthday = Birthday("15.03.1990")
        assert birthday.value == date(1990, 3, 15)

    def test_init_with_leap_year_date(self):
        """Test Birthday initialization with leap year date."""
        birthday = Birthday("29.02.2000")
        assert birthday.value == date(2000, 2, 29)

    def test_str_representation(self):
        """Test string representation of Birthday."""
        birthday = Birthday("01.01.2000")
        assert str(birthday) == "01.01.2000"

    def test_value_attribute_access(self):
        """Test accessing the value attribute."""
        birthday = Birthday("25.12.1995")
        assert birthday.value == date(1995, 12, 25)

    def test_raises_error_on_invalid_format(self):
        """Test that Birthday raises ValueError for invalid date format."""
        invalid_formats = [
            "1990-03-15",  # Wrong separator
            "03/15/1990",  # Wrong separator and order
            "15-03-1990",  # Wrong separator
            "15.03.90",    # Two-digit year
            "invalid"       # Not a date
        ]

        for invalid_date in invalid_formats:
            try:
                Birthday(invalid_date)
                assert False, f"Expected ValueError for date: {invalid_date}"
            except ValueError as e:
                assert "Invalid date format" in str(e)

    def test_raises_error_on_invalid_date(self):
        """Test that Birthday raises ValueError for non-existent dates."""
        invalid_dates = [
            "32.01.2000",  # Invalid day
            "31.02.2000",  # February doesn't have 31 days
            "29.02.2001",  # Not a leap year
            "00.01.2000",  # Day cannot be 00
            "01.13.2000",  # Invalid month
        ]

        for invalid_date in invalid_dates:
            try:
                Birthday(invalid_date)
                assert False, f"Expected ValueError for invalid date: {invalid_date}"
            except ValueError as e:
                assert "Invalid date format" in str(e)

    def test_different_date_formats_still_rejected(self):
        """Test that various incorrect formats are properly rejected."""
        invalid_formats = [
            "",
            "hello",
            "12.25.2000",  # Month 25
            "2020.01.01"   # Reversed order
        ]

        for invalid_date in invalid_formats:
            try:
                Birthday(invalid_date)
                assert False, f"Expected ValueError for: {invalid_date}"
            except ValueError:
                pass  # Expected
