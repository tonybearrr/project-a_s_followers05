import pickle
from models.address_book import AddressBook
from models.notebook import NoteBook


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


def save_notes(notebook: NoteBook, filename="notes.pkl"):
    """
    Save the notebook to a file.

    Args:
        notebook (NoteBook): Notebook instance
        filename (str): Name of the file to save to
    """
    with open(filename, "wb") as f:
        pickle.dump(notebook, f)


def load_notes(filename="notes.pkl"):
    """
    Load the notebook from a file.

    Args:
        filename (str): Name of the file to load from

    Returns:
        NoteBook: Notebook instance (empty if file not found)
    """
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return NoteBook()
