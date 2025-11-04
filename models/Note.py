import uuid
from datetime import datetime


class Note:
    def __init__(self, text, tags=None):
        """
        Initializes a new note.

        Args:
            text (str): Note text (required, cannot be empty)
            tags (list[str], optional): List of tags. Defaults to None.

        Raises:
            ValueError: If text is empty
        """
        if not text or not text.strip():
            raise ValueError("Note text cannot be empty")

        self._uuid = str(uuid.uuid4())
        self.text = text
        # Create a copy of the tags list to avoid external modifications
        self.tags = list(tags) if tags is not None else []
        # Use the same timestamp for both created_at and updated_at
        current_time = datetime.now()
        self.created_at = current_time
        self.updated_at = current_time

    def __str__(self):
        """
        Returns a formatted string representation of the note.

        Returns:
            str: String in format "Note text | Tags: tag1, tag2"
                 or "Note text | Tags: no tags"
        """
        if self.tags:
            tags_str = ", ".join(self.tags)
        else:
            tags_str = "no tags"

        return f"{self.text} | Tags: {tags_str}"

    def add_tag(self, tag):
        """
        Adds a tag to the note.

        Args:
            tag (str): Tag to add
        """
        if tag not in self.tags:
            self.tags.append(tag)
            self.updated_at = datetime.now()

    def remove_tag(self, tag):
        """
        Removes a tag from the note.

        Args:
            tag (str): Tag to remove
        """
        if tag in self.tags:
            self.tags.remove(tag)
            self.updated_at = datetime.now()

    def edit_tags(self, new_tags):
        """
        Replaces all tags with new ones.

        Args:
            new_tags (list[str]): New list of tags
        """
        self.tags = list(new_tags) if new_tags is not None else []
        self.updated_at = datetime.now()