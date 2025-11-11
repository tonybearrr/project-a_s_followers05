"""
Tests for the Address class.

This module contains tests for address field functionality.
"""

from models.address import Address


class TestAddress:
    """Test suite for the Address class."""

    def test_init_with_valid_address(self):
        """Test Address initialization with valid address."""
        address = Address("123 Main Street, Apt 4B")
        assert address.value == "123 Main Street, Apt 4B"

    def test_init_strips_whitespace(self):
        """Test that Address initialization strips leading and trailing whitespace."""
        address = Address("  123 Main Street  ")
        assert address.value == "123 Main Street"

    def test_init_raises_error_on_empty_string(self):
        """Test that empty string raises ValueError."""
        try:
            Address("")
            assert False, "Expected ValueError for empty address"
        except ValueError as e:
            assert "Address cannot be empty" in str(e)

    def test_init_raises_error_on_whitespace_only(self):
        """Test that whitespace-only string raises ValueError."""
        try:
            Address("   ")
            assert False, "Expected ValueError for whitespace-only address"
        except ValueError as e:
            assert "Address cannot be empty" in str(e)

    def test_str_representation(self):
        """Test string representation of Address."""
        address = Address("456 Oak Avenue")
        assert str(address) == "456 Oak Avenue"

    def test_multiline_address(self):
        """Test address with multiple lines."""
        address = Address("123 Main St\nApt 5\nNew York, NY 10001")
        assert "\n" in address.value
        assert "123 Main St" in address.value

    def test_address_with_special_characters(self):
        """Test address with special characters."""
        address = Address("Apt #42, St. O'Brien's Lane")
        assert address.value == "Apt #42, St. O'Brien's Lane"

    def test_very_long_address(self):
        """Test that very long addresses are accepted."""
        long_address = "Building A, Floor 25, Office 2501, 1234 Very Long Street Name Avenue, Suite 100-200, Business District, Metropolitan City, State Province, Country Name, Postal Code 12345-6789"
        address = Address(long_address)
        assert address.value == long_address

    def test_address_with_numbers_only(self):
        """Test address that consists only of numbers."""
        address = Address("12345")
        assert address.value == "12345"

    def test_unicode_address(self):
        """Test address with unicode characters."""
        address = Address("вул. Хрещатик, 1, Київ")
        assert address.value == "вул. Хрещатик, 1, Київ"

    def test_changing_adrress(self):
        """Test address changing"""
        address = Address("456 Oak Avenue")
        address = Address("228 Soap Avenue")
        assert address.value == "228 Soap Avenue"

    def test_removing_address(self):
        """Test address removing"""
        address = Address("456 Oak Avenue")
        address.value = None
        assert address.value is None
