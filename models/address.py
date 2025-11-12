"""
Address class for contact records.

This module provides the Address class that represents a contact's address
with basic validation.
"""

from .field import Field


class Address(Field):
    """
    Address field for a contact.

    Stores and validates address information.

    Attributes:
        value (str): The address text
    """

    def __init__(self, value):
        """
        Initialize an Address instance.

        Args:
            value (str): Address text

        Raises:
            ValueError: If address is empty or contains only whitespace
        """

        if not value or not value.strip():
            raise ValueError("Address cannot be empty")
        super().__init__(value.strip())

    # def __str__(self):
    #     """
    #     Return string representation of the address.

    #     Returns:
    #         str: The address value
    #     """
    #     return self.value
