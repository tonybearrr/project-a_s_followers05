"""
AddressBook class for managing contacts.

This module provides the AddressBook class that extends UserDict
to manage a collection of contact records with additional functionality
for birthday management.
"""

from collections import UserDict
from datetime import datetime, timedelta


class AddressBook(UserDict):
    """
    Address book for managing contact records.

    Extends UserDict to provide a dictionary-like interface for storing
    and managing contact records with additional birthday functionality.

    Attributes:
        data (dict): Dictionary storing contact records by name
    """

    def add_record(self, record):
        """
        Add a contact record to the address book.

        Args:
            record (Record): Contact record to add
        """
        self.data[record.name.value] = record

    def delete(self, name):
        """
        Delete a contact from the address book.

        Args:
            name (str): Name of the contact to delete

        Returns:
            Record: The deleted contact record

        Raises:
            KeyError: If contact with given name is not found
        """
        if name in self.data:
            record = self.data[name]
            del self.data[name]
            return record
        raise KeyError(f"Contact '{name}' not found")

    def find(self, name):
        """
        Find a contact by name.

        Args:
            name (str): Name of the contact to find

        Returns:
            Record or None: Contact record if found, None otherwise
        """
        if name in self.data:
            return self.data[name]

    def get_upcoming_birthdays(self):
        """
        Get contacts with birthdays in the next 7 days.

        Returns a list of contacts whose birthdays fall within the next 7 days,
        including today. Weekend birthdays are moved to the following Monday.

        Returns:
            list: List of tuples (name, congratulation_date) for upcoming birthdays
        """
        today = datetime.today().date()
        result = []

        for record in self.data.values():
            if record.birthday:
                birthday_this_year = record.birthday.value.replace(year=today.year)

                if birthday_this_year < today:
                    birthday_this_year = birthday_this_year.replace(year=today.year + 1)

                days_until_birthday = (birthday_this_year - today).days

                if 0 <= days_until_birthday <= 7:
                    congratulation_date = birthday_this_year

                    if birthday_this_year.weekday() >= 5:
                        days_until_monday = 7 - birthday_this_year.weekday()
                        congratulation_date = birthday_this_year + timedelta(days=days_until_monday)

                    result.append((record.name.value,
                                   congratulation_date.strftime("%d.%m.%Y")))
        return result
