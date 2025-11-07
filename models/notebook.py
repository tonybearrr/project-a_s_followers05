"""Notebook model for managing notes with tags and search functionality."""

from typing import Optional
from models.note import Note


class NoteBook:
    """Notebook class for managing notes with tags and search functionality."""
    def __init__(self):
        """
        Initializes a new notebook.

        Attributes:
            notes (dict): Dictionary to store notes with note._uuid as key
        """
        self.notes = {}

    # CRUD Methods

    def add_note(self, note: Note) -> bool:
        """
        Adds a note to the notebook.
        If a note with the same UUID already exists, it will be updated with the new one.

        Args:
            note (Note): Note object to add

        Returns:
            bool: True if a new note was added, False if an existing note was updated

        Raises:
            TypeError: If note is not an instance of Note
        """
        if not isinstance(note, Note):
            raise TypeError("Only Note objects can be added to the notebook")

        already_exists = note._uuid in self.notes
        self.notes[note._uuid] = note

        return not already_exists

    def delete_note(self, note_id: str) -> bool:
        """
        Deletes a note by its internal ID.

        Args:
            note_id (str): UUID of the note to delete

        Returns:
            bool: True if note was deleted, False if note was not found
        """
        if note_id in self.notes:
            del self.notes[note_id]
            return True
        return False

    def get_all_notes(self, sort_by: str = "created", reverse: bool = True) -> list[Note]:
        """
        Gets all notes with sorting.

        Args:
            sort_by (str): Sorting method - "created", "updated", "text", or "tags"
            reverse (bool): Sort in reverse order (True for descending, False for ascending)

        Returns:
            list[Note]: Sorted list of all notes
        """
        notes_list = list(self.notes.values())

        if sort_by == "created":
            return sorted(notes_list, key=lambda n: n.created_at, reverse=reverse)
        elif sort_by == "updated":
            return sorted(notes_list, key=lambda n: n.updated_at, reverse=reverse)
        elif sort_by == "text":
            return sorted(notes_list, key=lambda n: n.text.lower(), reverse=reverse)
        elif sort_by == "tags":
            return sorted(notes_list, key=lambda n: (
                n.tags[0].lower() if n.tags else "\uffff"
            ), reverse=reverse)
        else:
            # Default to created
            return sorted(notes_list, key=lambda n: n.created_at, reverse=reverse)

    def get_note_by_number(self, number: int, sort_by: str = "created") -> Optional[Note]:
        """
        Gets a note by its number in the sorted list.

        Args:
            number (int): Position in the list (1-based index)
            sort_by (str): Sorting method

        Returns:
            Optional[Note]: Note at the given position or None if out of range
        """
        notes_list = self.get_all_notes(sort_by)

        if 1 <= number <= len(notes_list):
            return notes_list[number - 1]
        return None

    def get_note_id_by_number(self, number: int, sort_by: str = "created") -> Optional[str]:
        """
        Gets a note ID by its number in the sorted list.

        Args:
            number (int): Position in the list (1-based index)
            sort_by (str): Sorting method

        Returns:
            Optional[str]: Note UUID at the given position or None if out of range
        """
        note = self.get_note_by_number(number, sort_by)
        return note._uuid if note else None

    # Search Methods

    def find_note_by_text(self, text_fragment: str) -> Optional[Note]:
        """
        Finds the first note containing the text fragment.

        Args:
            text_fragment (str): Text to search for

        Returns:
            Optional[Note]: First note containing the text or None if not found
        """
        text_lower = text_fragment.lower()

        for note in self.notes.values():
            if text_lower in note.text.lower():
                return note
        return None

    def search_notes(self, query: str) -> list[Note]:
        """
        Searches notes by text and tags.

        Args:
            query (str): Search query

        Returns:
            list[Note]: List of notes matching the query (in text or tags)
        """
        query_lower = query.lower()
        results = []

        for note in self.notes.values():
            # Check if query is in text
            if query_lower in note.text.lower():
                results.append(note)
                continue

            # Check if query matches any tag
            for tag in note.tags:
                if query_lower in str(tag).lower():
                    results.append(note)
                    break

        return results

    def search_by_tags(self, tags: list[str]) -> list[Note]:
        """
        Searches notes that contain all specified tags.

        Args:
            tags (list[str]): List of tags to search for (all must be present)

        Returns:
            list[Note]: List of notes containing all specified tags
        """
        if not tags:
            return []

        results = []
        tags_lower = [str(tag).lower() for tag in tags]

        for note in self.notes.values():
            note_tags_lower = [str(tag).lower() for tag in note.tags]

            # Check if all search tags are in note tags
            if all(tag in note_tags_lower for tag in tags_lower):
                results.append(note)

        return results

    def __len__(self) -> int:
        """
        Returns the number of notes in the notebook.

        Returns:
            int: Number of notes
        """
        return len(self.notes)

    def __str__(self) -> str:
        """
        Returns a string representation of the notebook.

        Returns:
            str: String showing number of notes
        """
        return f"NoteBook with {len(self.notes)} note(s)"
