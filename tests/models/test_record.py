"""
Tests for the Record class.

This module contains tests for contact record management functionality.
"""

from models.record import Record


class TestRecord:
    """Test suite for the Record class."""

    def test_init_with_valid_name(self):
        """Test Record initialization with a valid name."""
        record = Record("John Doe")
        assert record.name.value == "John Doe"
        assert not record.phones
        assert record.email is None
        assert record.birthday is None

    def test_str_representation_no_phones_no_birthday(self):
        """Test string representation without phones, email and birthday."""
        record = Record("Test User")
        expected = "Contact name: Test User, phones: no phones, email: no email, birthday: no birthday"
        assert str(record) == expected

    def test_str_representation_with_phones(self):
        """Test string representation with phones."""
        record = Record("Test User")
        record.add_phone("1234567890")
        record.add_phone("0987654321")
        assert "1234567890" in str(record)
        assert "0987654321" in str(record)

    def test_str_representation_with_birthday(self):
        """Test string representation with birthday."""
        record = Record("Test User")
        record.add_birthday("01.01.2000")
        assert "01.01.2000" in str(record)

    def test_add_phone(self):
        """Test adding a phone number."""
        record = Record("John Doe")
        record.add_phone("1234567890")
        assert len(record.phones) == 1
        assert record.phones[0].value == "1234567890"

    def test_add_multiple_phones(self):
        """Test adding multiple phone numbers."""
        record = Record("John Doe")
        record.add_phone("1111111111")
        record.add_phone("2222222222")
        record.add_phone("3333333333")
        assert len(record.phones) == 3

    def test_add_phone_raises_error_on_invalid_phone(self):
        """Test that adding invalid phone raises ValueError."""
        record = Record("John Doe")
        try:
            record.add_phone("123")
            assert False, "Expected ValueError for invalid phone"
        except ValueError:
            pass  # Expected

    def test_edit_phone(self):
        """Test editing an existing phone number."""
        record = Record("John Doe")
        record.add_phone("1234567890")
        record.edit_phone("1234567890", "9876543210")
        assert len(record.phones) == 1
        assert record.phones[0].value == "9876543210"

    def test_edit_phone_raises_error_if_not_found(self):
        """Test that editing non-existent phone raises ValueError."""
        record = Record("John Doe")
        record.add_phone("1234567890")
        try:
            record.edit_phone("9999999999", "1111111111")
            assert False, "Expected ValueError for phone not found"
        except ValueError as e:
            assert "Phone 9999999999 not found" in str(e)

    def test_delete_phone(self):
        """Test deleting a phone number."""
        record = Record("John Doe")
        record.add_phone("1234567890")
        record.add_phone("0987654321")
        record.delete_phone("1234567890")
        assert len(record.phones) == 1
        assert record.phones[0].value == "0987654321"

    def test_delete_phone_not_found(self):
        """Test deleting non-existent phone does nothing."""
        record = Record("John Doe")
        record.add_phone("1234567890")
        record.delete_phone("9999999999")
        assert len(record.phones) == 1

    def test_find_phone(self):
        """Test finding an existing phone number."""
        record = Record("John Doe")
        record.add_phone("1234567890")
        phone = record.find_phone("1234567890")
        assert phone is not None
        assert phone.value == "1234567890"

    def test_find_phone_not_found(self):
        """Test finding non-existent phone returns None."""
        record = Record("John Doe")
        record.add_phone("1234567890")
        phone = record.find_phone("9999999999")
        assert phone is None

    def test_find_phone_with_different_formats(self):
        """Test finding phone number with different formats."""
        record = Record("John Doe")
        record.add_phone("099-4777-528")
        phone = record.find_phone("(099)-4777-528")
        assert phone is not None
        assert phone.value == "0994777528"

    def test_add_birthday(self):
        """Test adding a birthday."""
        record = Record("John Doe")
        record.add_birthday("15.03.1990")
        assert record.birthday is not None
        assert str(record.birthday) == "15.03.1990"

    def test_add_birthday_raises_error_on_invalid_format(self):
        """Test that adding invalid birthday format raises ValueError."""
        record = Record("John Doe")
        try:
            record.add_birthday("1990-03-15")
            assert False, "Expected ValueError for invalid birthday format"
        except ValueError as e:
            assert "Invalid date format" in str(e)

    def test_full_record_operations(self):
        """Test multiple operations on a record."""
        record = Record("Jane Smith")

        # Add phones
        record.add_phone("1111111111")
        record.add_phone("2222222222")

        # Edit phone
        record.edit_phone("1111111111", "3333333333")

        # Add birthday
        record.add_birthday("25.12.1995")

        # Verify state
        assert record.name.value == "Jane Smith"
        assert len(record.phones) == 2
        assert record.phones[0].value == "3333333333"
        assert str(record.birthday) == "25.12.1995"

    def test_record_with_multiple_phones_and_birthday(self):
        """Test record with multiple phones and birthday."""
        record = Record("Multi Phone User")
        record.add_phone("1111111111")
        record.add_phone("2222222222")
        record.add_phone("3333333333")
        record.add_birthday("01.01.2000")

        assert len(record.phones) == 3
        assert record.birthday is not None

    def test_add_email(self):
        """Test adding an email address."""
        record = Record("John Doe")
        record.add_email("test@example.com")
        assert record.email is not None
        assert record.email.value == "test@example.com"

    def test_update_email(self):
        """Test updating email address (replacing existing)."""
        record = Record("John Doe")
        record.add_email("old@example.com")
        assert record.email.value == "old@example.com"
        record.add_email("new@example.com")
        assert record.email.value == "new@example.com"

    def test_delete_email(self):
        """Test deleting email address."""
        record = Record("John Doe")
        record.add_email("test@example.com")
        assert record.email is not None
        record.delete_email()
        assert record.email is None

    def test_add_email_raises_error_on_invalid_email(self):
        """Test that adding invalid email raises ValueError."""
        record = Record("John Doe")
        try:
            record.add_email("invalid-email")
            assert False, "Expected ValueError for invalid email"
        except ValueError:
            pass  # Expected

    def test_str_representation_with_email(self):
        """Test string representation with email."""
        record = Record("Test User")
        record.add_email("test@example.com")
        assert "test@example.com" in str(record)

    def test_str_representation_with_email(self):
        """Test string representation with email."""
        record = Record("Test User")
        record.add_email("test@example.com")
        assert "test@example.com" in str(record)

    def test_record_with_phones_email_and_birthday(self):
        """Test record with phones, email and birthday."""
        record = Record("Complete User")
        record.add_phone("1111111111")
        record.add_email("user@example.com")
        record.add_birthday("01.01.2000")

        assert len(record.phones) == 1
        assert record.email is not None
        assert record.birthday is not None
        assert "1111111111" in str(record)
        assert "user@example.com" in str(record)
        assert "01.01.2000" in str(record)
        
    def test_add_address(self):
        """Test adding an address."""
        record = Record("John Doe")
        record.add_address("123 Main Street")
        assert record.address is not None
        assert record.address.value == "123 Main Street"

    def test_update_address(self):
        """Test updating an address (replacing existing)."""
        record = Record("John Doe")
        record.add_address("123 Main Street")
        assert record.address.value == "123 Main Street"
        record.add_address("528 Linkoln Avenue")
        assert record.address.value == "528 Linkoln Avenue"

    def test_delete_address(self):
        """Test deleting an address."""
        record = Record("John Doe")
        record.add_address("123 Main Street")
        assert record.address is not None
        record.remove_address()
        assert record.email is None

    def test_str_representation_with_address(self):
        """Test string representation with an address."""
        record = Record("John Doe")
        record.add_address("123 Main Street")
        assert "123 Main Street" in str(record)