"""
Birthday field class for the address book.

This module provides the Birthday class for storing and validating
birthday dates in the address book system.
"""

from datetime import datetime
from .Field import Field


class Birthday(Field):
    """
    Birthday field with validation.
    
    Validates that dates are in DD.MM.YYYY format and converts them to date objects.
    
    Attributes:
        value (date): The validated birthday date
    """

    def __init__(self, value):
        """
        Initialize a birthday field with validation.
        
        Args:
            value (str): Birthday date in DD.MM.YYYY format
            
        Raises:
            ValueError: If date format is invalid
        """
        try:
            date_value = datetime.strptime(value, "%d.%m.%Y").date()
            super().__init__(date_value)
        except ValueError as exc:
            raise ValueError("Invalid date format. Use DD.MM.YYYY") from exc

    def __str__(self):
        """
        Return string representation of the birthday.
        
        Returns:
            str: Birthday in DD.MM.YYYY format
        """
        return self.value.strftime("%d.%m.%Y")
