import tempfile
import os
from storage.file_storage import (
    save_data,
    load_data
)
from models.AddressBook import AddressBook
from models.Record import Record


class TestSaveAndLoadData:
    """Test suite for save_data and load_data functions."""

    def test_save_and_load_data(self):
        """Test saving and loading address book."""
        book = AddressBook()
        record = Record("John Doe")
        record.add_phone("1234567890")
        book.add_record(record)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pkl") as f:
            filename = f.name
            try:
                save_data(book, filename)
                loaded_book = load_data(filename)
                assert len(loaded_book.data) == 1
                assert "John Doe" in loaded_book.data
            finally:
                if os.path.exists(filename):
                    os.remove(filename)

    def test_load_data_file_not_found(self):
        """Test loading when file doesn't exist."""
        loaded_book = load_data("nonexistent.pkl")
        assert isinstance(loaded_book, AddressBook)
        assert len(loaded_book.data) == 0
