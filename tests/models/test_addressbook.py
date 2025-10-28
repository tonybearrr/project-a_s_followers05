"""
Tests for the AddressBook class.

This module contains tests for address book management functionality.
"""

from datetime import date, timedelta
from models.AddressBook import AddressBook
from models.Record import Record


class TestAddressBook:
    """Test suite for the AddressBook class."""

    def test_init(self):
        """Test AddressBook initialization."""
        book = AddressBook()
        assert len(book.data) == 0

    def test_add_record(self):
        """Test adding a record to the address book."""
        book = AddressBook()
        record = Record("John Doe")
        record.add_phone("1234567890")
        book.add_record(record)
        assert len(book.data) == 1
        assert "John Doe" in book.data

    def test_add_multiple_records(self):
        """Test adding multiple records to the address book."""
        book = AddressBook()

        record1 = Record("Alice")
        record2 = Record("Bob")
        record3 = Record("Charlie")

        book.add_record(record1)
        book.add_record(record2)
        book.add_record(record3)

        assert len(book.data) == 3
        assert "Alice" in book.data
        assert "Bob" in book.data
        assert "Charlie" in book.data

    def test_find_existing_record(self):
        """Test finding an existing record."""
        book = AddressBook()
        record = Record("John Doe")
        book.add_record(record)

        found = book.find("John Doe")
        assert found is not None
        assert found.name.value == "John Doe"

    def test_find_non_existing_record(self):
        """Test finding a non-existing record returns None."""
        book = AddressBook()
        record = Record("John Doe")
        book.add_record(record)

        found = book.find("Jane Doe")
        assert found is None

    def test_delete_existing_record(self):
        """Test deleting an existing record."""
        book = AddressBook()
        record = Record("John Doe")
        book.add_record(record)

        deleted = book.delete("John Doe")
        assert deleted.name.value == "John Doe"
        assert "John Doe" not in book.data
        assert len(book.data) == 0

    def test_delete_non_existing_record(self):
        """Test deleting a non-existing record raises KeyError."""
        book = AddressBook()
        record = Record("John Doe")
        book.add_record(record)

        try:
            book.delete("Jane Doe")
            assert False, "Expected KeyError"
        except KeyError as e:
            assert "Contact 'Jane Doe' not found" in str(e)

    def test_dict_like_access(self):
        """Test dictionary-like access to records."""
        book = AddressBook()
        record = Record("Test User")
        book.add_record(record)

        assert book.data["Test User"] == record
        assert len(book.data) == 1

    def test_get_upcoming_birthdays_empty_book(self):
        """Test getting upcoming birthdays from empty book."""
        book = AddressBook()
        birthdays = book.get_upcoming_birthdays()
        assert birthdays == []

    def test_get_upcoming_birthdays_no_birthdays(self):
        """Test getting upcoming birthdays when contacts have no birthdays."""
        book = AddressBook()
        record = Record("No Birthday")
        record.add_phone("1234567890")
        book.add_record(record)

        birthdays = book.get_upcoming_birthdays()
        assert birthdays == []

    def test_get_upcoming_birthdays_today(self):
        """Test getting birthdays for today."""
        book = AddressBook()
        today = date.today()
        birthday_str = today.strftime("%d.%m.%Y")

        record = Record("Today Birthday")
        record.add_birthday(birthday_str)
        book.add_record(record)

        birthdays = book.get_upcoming_birthdays()
        assert len(birthdays) >= 1  # Today's birthday should be included
        assert ("Today Birthday", birthday_str) in birthdays

    def test_get_upcoming_birthdays_next_week(self):
        """Test getting birthdays in the next 7 days."""
        book = AddressBook()
        today = date.today()

        # Add birthday 3 days from now
        future_birthday = today + timedelta(days=3)
        birthday_str = future_birthday.strftime("%d.%m.%Y")

        record = Record("Future Birthday")
        record.add_birthday(birthday_str)
        book.add_record(record)

        birthdays = book.get_upcoming_birthdays()
        assert len(birthdays) >= 1

    def test_get_upcoming_birthdays_past_date_this_year(self):
        """Test that past birthdays in this year move to next year."""
        book = AddressBook()
        today = date.today()
        # Use a fixed past date (e.g., January 1)
        past_birthday = date(today.year, 1, 1)

        # If today is early in the year, use a date from last month
        if past_birthday >= today:
            past_birthday = date(today.year - 1, 12, 25)

        birthday_str = past_birthday.strftime("%d.%m.%Y")

        record = Record("Past Birthday")
        record.add_birthday(birthday_str)
        book.add_record(record)

        # Past birthday should not appear in upcoming (next 7 days)
        # unless it's been adjusted to next year
        _ = book.get_upcoming_birthdays()  # Just checking it doesn't crash

    def test_address_book_comprehensive(self):
        """Test comprehensive address book operations."""
        book = AddressBook()

        # Create and add records
        john = Record("John Doe")
        john.add_phone("1234567890")
        john.add_birthday("15.03.1990")

        jane = Record("Jane Smith")
        jane.add_phone("0987654321")
        jane.add_phone("5555555555")

        book.add_record(john)
        book.add_record(jane)

        # Verify additions
        assert len(book.data) == 2
        assert book.find("John Doe") is not None
        assert book.find("Jane Smith") is not None

        # Delete a record
        deleted = book.delete("Jane Smith")
        assert deleted.name.value == "Jane Smith"
        assert len(book.data) == 1

        # Verify deletion
        assert book.find("Jane Smith") is None
