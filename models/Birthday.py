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


    Validates that dates are in DD.MM.YYYY
    format and converts them to date objects.

    Attributes:
        value (date): The validated birthday date
    """
    DATE_FORMAT = "%d.%m.%Y"
    DATE_FORMAT_DISPLAY = "DD.MM.YYYY"

    def __init__(self, value: str):
        """
        Initialize a birthday field with validation.

        Args:
            value (str): Birthday date in DD.MM.YYYY format

        Raises:
            ValueError: If date format is invalid
        """
        try:
            date_value = datetime.strptime(value, Birthday.DATE_FORMAT).date()
            super().__init__(date_value)
        except ValueError:
            raise ValueError(f"""Invalid date format. Use {Birthday.DATE_FORMAT_DISPLAY} format.""")

    def __str__(self):
        """
        Return string representation of the birthday.

        Returns:
            str: Birthday in DD.MM.YYYY format
        """
        return self.value.strftime(Birthday.DATE_FORMAT)
