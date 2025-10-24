"""
Name field class for the address book.

This module provides the Name class for storing and validating
contact names in the address book system.
"""

from .Field import Field


class Name(Field):
    """
    Name field with validation.
    
    Validates that names are not empty.
    
    Attributes:
        value (str): The validated name
    """

    def __init__(self, value):
        """
        Initialize a name field with validation.
        
        Args:
            value (str): Name to validate and store
            
        Raises:
            ValueError: If name is empty
        """
        if not value:
            raise ValueError("Name cannot be empty")
        super().__init__(value)
