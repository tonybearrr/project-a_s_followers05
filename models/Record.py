"""
Record class for the address book.

This module provides the Record class that represents a single contact
with name, phone numbers, and birthday information.
"""

from .Phone import Phone
from .Name import Name
from .Birthday import Birthday


class Record:
    """
    A record representing a single contact in the address book.
    
    Contains contact information including name, phone numbers, and birthday.
    
    Attributes:
        name (Name): Contact's name
        phones (list): List of Phone objects
        birthday (Birthday, optional): Contact's birthday
    """

    def __init__(self, name):
        """
        Initialize a new contact record.
        
        Args:
            name (str): Contact's name
        """
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def __str__(self):
        """
        Return string representation of the contact.
        
        Returns:
            str: Formatted contact information
        """
        phones = "; ".join(p.value for p in self.phones) if self.phones else "no phones"
        bday = self.birthday if self.birthday else "no birthday"
        return f"Contact name: {self.name.value}, phones: {phones}, birthday: {bday}"

    def add_phone(self, phone):
        """
        Add a phone number to the contact.
        
        Args:
            phone (str): Phone number to add
            
        Raises:
            ValueError: If phone number format is invalid
        """
        self.phones.append(Phone(phone))

    def edit_phone(self, old_phone, new_phone):
        """
        Edit an existing phone number.
        
        Args:
            old_phone (str): Current phone number to replace
            new_phone (str): New phone number
            
        Raises:
            ValueError: If old phone number is not found or new phone format is invalid
        """
        phone = self.find_phone(old_phone)
        if not phone:
            raise ValueError(f"Phone {old_phone} not found")
        for idx, phone in enumerate(self.phones):
            if phone.value == old_phone:
                self.phones[idx] = Phone(new_phone)

    def delete_phone(self, phone_number):
        """
        Delete a phone number from the contact.
        
        Args:
            phone_number (str): Phone number to delete
        """
        phone = self.find_phone(phone_number)
        if phone:
            self.phones.remove(phone)
        
    def find_phone(self, phone):
        """
        Find a phone number in the contact's phone list.
        
        Args:
            phone (str): Phone number to find
            
        Returns:
            Phone or None: Phone object if found, None otherwise
        """
        for phone_number in self.phones:
            if phone_number.value == phone:
                return phone_number
        return None

    def add_birthday(self, birthday):
        """
        Add birthday to the contact.
        
        Args:
            birthday (str): Birthday in DD.MM.YYYY format
            
        Raises:
            ValueError: If birthday format is invalid
        """
        self.birthday = Birthday(birthday)
