import pickle
from models.AddressBook import AddressBook


def save_data(book, filename="addressbook.pkl"):
    """
    Save the address book to a file.

    Args:
        book (AddressBook): Address book instance
        filename (str): Name of the file to save to
    """
    with open(filename, "wb") as f:
        pickle.dump(book, f)


def load_data(filename="addressbook.pkl"):
    """
    Load the address book from a file.

    Args:
        filename (str): Name of the file to load from

    Returns:
        AddressBook: Address book instance
    """
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()
