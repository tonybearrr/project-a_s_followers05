"""
Tests for the handlers module.

This module contains tests for all handler functions in the address book bot.
"""
from core.handlers import (
    add_contact,
    update_contact,
    get_all_contacts,
    get_one_contact,
    delete_contact,
    add_birthday,
    show_birthday,
    birthdays
)
from models.AddressBook import AddressBook
from models.Record import Record


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
        assert "Enter the argument for the command" in result or "Invalid date format" in result


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

    def test_birthdays_no_upcoming(self):
        """Test birthdays when no upcoming birthdays."""
        book = AddressBook()
        result = birthdays(book)
        assert "No birthdays in the next 7 days" in result

    def test_birthdays_with_upcoming(self):
        """Test birthdays with upcoming birthdays."""
        book = AddressBook()
        from datetime import date, timedelta
        today = date.today()
        future_birthday = (today + timedelta(days=3)).strftime("%d.%m.%Y")
        record = Record("John Doe")
        record.add_birthday(future_birthday)
        book.add_record(record)
        result = birthdays(book)
        assert "John Doe" in result
