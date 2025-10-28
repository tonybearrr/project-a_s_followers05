"""
Phone field class for the address book.

This module provides the Phone class for storing and validating
phone numbers in the address book system.
"""

from .Field import Field


class Phone(Field):
    """
    Phone number field with validation.
    
    Validates that phone numbers are exactly 10 digits and contain only numbers.
    
    Attributes:
        value (str): The validated phone number
    """

    def __init__(self, value):
        """
        Initialize a phone field with validation.
        
        Args:
            value (str): Phone number to validate and store
            
        Raises:
            ValueError: If phone number is not 10 digits or contains non-numeric characters
        """
        if not (value.isdigit() and len(value) == 10):
            raise ValueError("Phone number must be 10 digits and contain only numbers")
        super().__init__(value)
