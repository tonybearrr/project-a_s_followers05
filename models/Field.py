"""
Base field class for the address book.

This module provides the base Field class that serves as a parent
for all field types in the address book system.
"""


class Field:
    """
    Base field class for storing and displaying values.
    
    This is the parent class for all field types (Name, Phone, Birthday).
    It provides basic functionality for storing and string representation.
    
    Attributes:
        value: The stored value of the field
    """

    def __init__(self, value):
        """
        Initialize a field with a value.
        
        Args:
            value: The value to store in the field
        """
        self.value = value

    def __str__(self):
        """
        Return string representation of the field value.
        
        Returns:
            str: String representation of the value
        """
        return str(self.value)
