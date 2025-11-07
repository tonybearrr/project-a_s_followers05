"""
AddressBook class for managing contacts.

This module provides the AddressBook class that extends UserDict
to manage a collection of contact records with additional functionality
for birthday management.
"""

from collections import UserDict
from datetime import date, datetime, timedelta
from models.birthday import Birthday
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
        return self.data[name] if name in self.data else None

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

        searched_records = []

        for record in self.data.values():
            for r in record.phones:
                match = re.search(phone, r.value)
                if match:
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
            if record.email is not None:
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

    def get_upcoming_birthdays(
        self, days_ahead: int = 7, now_date: date = datetime.now().date()
    ):
        """
        Return upcoming birthdays within a given time window.
        Scans all records in the address book and returns a mapping of record names to
        their corresponding record objects for those whose next birthday falls within
        the next `days_ahead` days (including today).
        Behavior:
        - For each record with a non-None birthday, the birthday date is adjusted to the
            current year (using now_date.year) to produce the next occurrence.
        - If that adjusted date is earlier than now_date, the birthday is considered to
            fall in the next calendar year (year + 1).
        - If the (current-year) birthday has not yet occurred and falls on a weekend
            (Saturday or Sunday), the function moves the observed birthday forward to the
            following Monday before counting days until the birthday.
        - The function computes days_until_birthday = (adjusted_birthday - now_date).days
            and includes the record when 0 <= days_until_birthday <= days_ahead.
        Parameters:
        - days_ahead (int): Number of days ahead (inclusive) to look for upcoming
            birthdays. Default: 7.
        - now_date (date or datetime, optional): Reference date from which to compute
            upcoming birthdays. If not provided, the current date is used.
        Returns:
        - dict: A dictionary mapping string names (record.name.value) to their record
            objects for all records whose next birthday (after the adjustments above)
            falls within the next `days_ahead` days.
        Notes and assumptions:
        - Records without a birthday (record.birthday is None) are ignored.
        - The function expects record.birthday.value to be a date-like object with a
            year and weekday() method.
        - Weekend adjustment (moving to Monday) is applied when the birthday for the
            current year has not yet passed; birthdays that are bumped to the next year
            are not subject to the same weekend-to-Monday adjustment in the current logic.
        """

        if now_date is None:
            now_date = datetime.now()

        result = []

        for record in self.data.values():
            if record.birthday is not None:
                birth_date = record.birthday

                this_year_birthday = birth_date.value.replace(year=now_date.year)
                # If birthday has already occurred this year, consider next year's birthday
                if this_year_birthday < now_date:
                    this_year_birthday = this_year_birthday.replace(
                        year=now_date.year + 1
                    )
                else:
                    this_year_birthday_weekday = this_year_birthday.weekday()

                    # Adjust for weekends (Saturday and Sunday)
                    if this_year_birthday_weekday == 6:  # Sunday
                        this_year_birthday += timedelta(days=1)  # Move to Monday
                    elif this_year_birthday_weekday == 5:  # Saturday
                        this_year_birthday += timedelta(days=2)  # Move to Monday

                    days_until_birthday = (this_year_birthday - now_date).days

                    if 0 <= days_until_birthday <= days_ahead:
                        result.append(
                            (
                                record.name.value,
                                record.birthday.value.strftime(Birthday.DATE_FORMAT),
                            )
                        )

        return result
