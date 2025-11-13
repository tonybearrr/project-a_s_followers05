"""
Email field class for the address book.

This module provides the Email class for storing and validating
email addresses in the address book system.
"""
import re
from colorama import Fore, Style
from .field import Field


class Email(Field):
    """
    Email address field with validation.

    Validates that email addresses follow standard email format.

    Attributes:
        value (str): The validated email address
    """
    EMAIL_PATTERN = re.compile(
        r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    )

    def __init__(self, value):
        """
        Initialize an email field with validation.

        Args:
            value (str): Email address to validate and store

        Raises:
            ValueError: If email address format is invalid
        """
        if not value or not value.strip():
            raise ValueError("Email address cannot be empty")

        email = value.strip().lower()

        if not Email.EMAIL_PATTERN.match(email):
            raise ValueError(f"Invalid email format. Use format: {Fore.YELLOW}user@domain.com{Style.RESET_ALL}")

        super().__init__(email)
