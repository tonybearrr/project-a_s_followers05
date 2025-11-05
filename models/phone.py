"""
Phone field class for the address book.

This module provides the Phone class for storing and validating
phone numbers in the address book system.
"""
import re
from .field import Field


class Phone(Field):
    """
    Phone number field with validation.

    Validates that phone numbers are exactly 10 digits and contain only numbers.

    Attributes:
        value (str): The validated phone number
    """
    PHONE_LEN = 10
    EMPTY_PHONE = ""

    def __init__(self, value):
        """
        Initialize a phone field with validation.

        Args:
            value (str): Phone number to validate and store

        Raises:
            ValueError: If phone number is not 10 digits or contains non-numeric characters
        """
        # Clean the phone number (remove all non-digit characters)
        phone = re.sub(r"\D", "", value)
        if phone == Phone.EMPTY_PHONE:
            raise ValueError("Phone number cannot be empty")

        if not (phone.isdigit() and len(phone) == Phone.PHONE_LEN):
            raise ValueError(f"""Phone number must be {Phone.PHONE_LEN} digits and contain only digits""")

        super().__init__(phone)
