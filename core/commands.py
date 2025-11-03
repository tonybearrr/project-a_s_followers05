
from enum import StrEnum


class Command(StrEnum):
    ADD_CONTACT = "add"
    UPDATE_CONTACT = "change"
    SHOW_CONTACT = "phone"
    SHOW_ALL_CONTACTS = "all"
    ADD_BIRTHDAY = "add-birthday"
    SHOW_BIRTHDAY = "show-birthday"
    SHOW_UPCOMING_BIRTHDAYS = "birthdays"
    DELETE_CONTACT = "delete"
    HELLO = "hello"
    HELP = "help"
    HELP_ALT = "?"
    EXIT_1 = "exit"
    EXIT_2 = "close"
