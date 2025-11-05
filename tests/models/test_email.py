"""
Tests for the Email class.

This module contains tests for the Email field validation functionality.
"""

from models.email import Email


class TestEmail:
    """Test suite for the Email class."""

    def test_init_with_valid_email(self):
        """Test Email initialization with valid email."""
        email = Email("test@example.com")
        assert email.value == "test@example.com"

    def test_init_with_uppercase_email(self):
        """Test Email normalization (lowercase)."""
        email = Email("Test@Example.COM")
        assert email.value == "test@example.com"  # Lowercase

    def test_init_with_spaces(self):
        """Test Email with spaces (trimmed)."""
        email = Email("  test@example.com  ")
        assert email.value == "test@example.com"

    def test_init_with_various_valid_formats(self):
        """Test Email with various valid email formats."""
        valid_emails = [
            "user@domain.com",
            "user.name@domain.com",
            "user_name@domain.com",
            "user+tag@domain.com",
            "user123@domain123.com",
            "user@subdomain.domain.com",
        ]
        for valid_email in valid_emails:
            email = Email(valid_email)
            assert email.value == valid_email.lower()

    def test_raises_error_on_invalid_format(self):
        """Test that Email raises ValueError for invalid format."""
        invalid_emails = [
            "invalid",           # No @
            "@example.com",      # No user
            "user@",             # No domain
            "user@domain",       # No TLD
            "user@domain.",      # No TLD
            "user @domain.com",  # Space in email
            "user@domain .com",  # Space in domain
            "user@@domain.com",  # Double @
            "user@domain@com",   # Multiple @
        ]
        for invalid_email in invalid_emails:
            try:
                Email(invalid_email)
                assert False, f"Expected ValueError for email: {invalid_email}"
            except ValueError as e:
                assert "Invalid email format" in str(e) or "cannot be empty" in str(e)

    def test_raises_error_on_empty_string(self):
        """Test that Email raises ValueError for empty string."""
        try:
            Email("")
            assert False, "Expected ValueError for empty string"
        except ValueError as e:
            assert "cannot be empty" in str(e)

    def test_raises_error_on_whitespace_only(self):
        """Test that Email raises ValueError for whitespace only."""
        try:
            Email("   ")
            assert False, "Expected ValueError for whitespace only"
        except ValueError as e:
            assert "cannot be empty" in str(e)

    def test_str_representation(self):
        """Test string representation of Email."""
        email = Email("test@example.com")
        assert str(email) == "test@example.com"

    def test_value_attribute_access(self):
        """Test accessing the value attribute."""
        email = Email("user@domain.com")
        assert email.value == "user@domain.com"
