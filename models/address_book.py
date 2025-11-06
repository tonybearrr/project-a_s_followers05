"""
AddressBook class for managing contacts.

This module provides the AddressBook class that extends UserDict
to manage a collection of contact records with additional functionality
for birthday management.
"""

from collections import UserDict
from models.birthday import Birthday
from models.email import Email
from models.phone import Phone
from datetime import datetime, timedelta
import re


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

    def search_contacts_by_name(self, name):
        """
        Find a contact by name.

        Args:
            name (str): Name of the contact to find

        Returns:
            List of Records or None: Contact record if found, None otherwise
        """
        searched_records = []
        name_lower = name.lower()
        for record in self.data.values():
            match = re.search(name_lower, record.name.value.lower())
            if match:
                searched_records.append(record)
        
        return set(searched_records)
        
    def search_contacts_by_phone(self, phone):
        """
        Find a contact by phone.

        Args:
            phone (str): Phone in the contact to find

        Returns:
            List of the records or None: List of the Contacts if found, None otherwise
        """
        # obj_phone = Phone(phone)
        searched_records = []

        for record in self.data.values():
            for r in record.phones:
                match = re.search(phone, r.value)
                if match:
                # if phone == p.value:
                    searched_records.append(record)
        return set(searched_records)
    
    def search_contacts_by_email(self, email):
        """
        Find a contact by email.

        Args:
            email (str): Email of the contact to find

        Returns:
            List of the records or None: List of the Contacts if found, None otherwise
        """

        searched_records = []
        email_lower = email.lower()

        for record in self.data.values():
            if record.email != None:
                match = re.search(email_lower, record.email.value.lower())
                if match:
                    searched_records.append(record)
        return set(searched_records)
    
    def search_contacts_by_address(self, address):
        """
        Find a contact by address.

        Args:
            address (str): Address of the contact to find

        Returns:
            List of the records or None: List of the Contacts if found, None otherwise
        """
        pass
        # searched_records = []
        # address_lower = address.lower()

        # for record in self.data.values():
        #     if record.address != None:
        #         match = re.search(address_lower, record.address.value.lower())
        #         if match: 
        #             searched_records.append(record)
        # return set(searched_records)

    def get_upcoming_birthdays(self):
        """
        Get contacts with birthdays in the next 7 days.

        Returns a list of contacts whose birthdays fall within the next 7 days,
        including today. Weekend birthdays are moved to the following Monday.

        Returns:
            list: List of tuples (name, congratulation_date) for upcoming
            birthdays
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
                                   congratulation_date.strftime(Birthday.DATE_FORMAT)))
        return result
