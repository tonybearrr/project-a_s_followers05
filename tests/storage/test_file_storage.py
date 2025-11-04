import tempfile
import os

from core.handlers import add_note
from models.notebook import NoteBook
from storage.file_storage import (
    save_data,
    load_data, load_notes, save_notes
)
from models.address_book import AddressBook
from models.record import Record


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


class TestSaveAndLoadNotes:
    """Test suite for save_notes and load_notes functions."""

    def test_save_and_load_notes(self):
        """Test saving and loading notebook."""
        notebook = NoteBook()
        add_note(["Test note 1", "tag1"], notebook)
        add_note(["Test note 2", "tag2"], notebook)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pkl") as f:
            filename = f.name

        try:
            save_notes(notebook, filename)
            loaded_notebook = load_notes(filename)

            assert len(loaded_notebook) == 2
            notes = loaded_notebook.get_all_notes()
            assert any("Test note 1" in note.text for note in notes)
            assert any("Test note 2" in note.text for note in notes)
        finally:
            if os.path.exists(filename):
                os.remove(filename)

    def test_load_notes_file_not_found(self):
        """Test loading when file doesn't exist."""
        loaded_notebook = load_notes("nonexistent_notes.pkl")
        assert isinstance(loaded_notebook, NoteBook)
        assert len(loaded_notebook) == 0

    def test_save_empty_notebook(self):
        """Test saving empty notebook."""
        notebook = NoteBook()

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pkl") as f:
            filename = f.name

        try:
            save_notes(notebook, filename)
            loaded_notebook = load_notes(filename)
            assert len(loaded_notebook) == 0
        finally:
            if os.path.exists(filename):
                os.remove(filename)

    def test_save_notes_with_complex_data(self):
        """Test saving notes with complex data."""
        notebook = NoteBook()
        add_note(["Note with unicode: 你好", "тег,tag"], notebook)
        add_note(["Note with special chars: !@#$%"], notebook)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pkl") as f:
            filename = f.name

        try:
            save_notes(notebook, filename)
            loaded_notebook = load_notes(filename)
            assert len(loaded_notebook) == 2
        finally:
            if os.path.exists(filename):
                os.remove(filename)

    def test_save_and_load_preserves_timestamps(self):
        """Test that save/load preserves timestamps."""
        notebook = NoteBook()
        add_note(["Test note"], notebook)
        original_notes = notebook.get_all_notes()
        original_created = original_notes[0].created_at
        original_updated = original_notes[0].updated_at

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pkl") as f:
            filename = f.name

        try:
            save_notes(notebook, filename)
            loaded_notebook = load_notes(filename)
            loaded_notes = loaded_notebook.get_all_notes()

            assert loaded_notes[0].created_at == original_created
            assert loaded_notes[0].updated_at == original_updated
        finally:
            if os.path.exists(filename):
                os.remove(filename)

    def test_save_notes_default_filename(self):
        """Test saving with default filename."""
        notebook = NoteBook()
        add_note(["Test"], notebook)

        try:
            save_notes(notebook)
            loaded_notebook = load_notes()
            assert len(loaded_notebook) == 1
        finally:
            if os.path.exists("notes.pkl"):
                os.remove("notes.pkl")
