import pytest
from datetime import datetime
import time
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from models.Note import Note


# Tests for Note initialization

def test_init_with_text_only():
    """Test creating a note with only text"""
    note = Note("Test note")

    assert note.text == "Test note"
    assert note.tags == []
    assert isinstance(note._uuid, str)
    assert len(note._uuid) == 36  # UUID4 length with hyphens
    assert isinstance(note.created_at, datetime)
    assert isinstance(note.updated_at, datetime)
    assert note.created_at == note.updated_at


def test_init_with_text_and_tags():
    """Test creating a note with text and tags"""
    tags = ["tag1", "tag2", "tag3"]
    note = Note("Test note", tags)

    assert note.text == "Test note"
    assert note.tags == ["tag1", "tag2", "tag3"]
    assert len(note._uuid) == 36


def test_init_with_empty_tags_list():
    """Test creating a note with empty tags list"""
    note = Note("Test note", [])

    assert note.text == "Test note"
    assert note.tags == []


def test_init_empty_text_raises_error():
    """Test that empty text raises ValueError"""
    with pytest.raises(ValueError) as exc_info:
        Note("")

    assert str(exc_info.value) == "Note text cannot be empty"


def test_init_whitespace_only_text_raises_error():
    """Test that whitespace-only text raises ValueError"""
    with pytest.raises(ValueError) as exc_info:
        Note("   ")

    assert str(exc_info.value) == "Note text cannot be empty"


def test_init_tab_and_newline_only_raises_error():
    """Test that text with only tabs and newlines raises ValueError"""
    with pytest.raises(ValueError) as exc_info:
        Note("\t\n\r  ")

    assert str(exc_info.value) == "Note text cannot be empty"


def test_init_none_text_raises_error():
    """Test that None as text raises ValueError"""
    with pytest.raises(ValueError) as exc_info:
        Note(None)

    assert str(exc_info.value) == "Note text cannot be empty"


def test_unique_uuid_for_different_notes():
    """Test that different notes have unique UUIDs"""
    note1 = Note("Note 1")
    note2 = Note("Note 2")

    assert note1._uuid != note2._uuid


# Tests for __str__ method

def test_str_with_no_tags():
    """Test string representation with no tags"""
    note = Note("My note")

    assert str(note) == "My note | Tags: no tags"


def test_str_with_single_tag():
    """Test string representation with single tag"""
    note = Note("My note", ["important"])

    assert str(note) == "My note | Tags: important"


def test_str_with_multiple_tags():
    """Test string representation with multiple tags"""
    note = Note("My note", ["important", "work", "urgent"])

    assert str(note) == "My note | Tags: important, work, urgent"


def test_str_with_empty_tags_list():
    """Test string representation with explicitly empty tags list"""
    note = Note("My note", [])

    assert str(note) == "My note | Tags: no tags"


def test_str_after_removing_all_tags():
    """Test string representation after removing all tags"""
    note = Note("My note", ["tag1"])
    note.remove_tag("tag1")

    assert str(note) == "My note | Tags: no tags"


# Tests for add_tag method

def test_add_tag_to_empty_list():
    """Test adding a tag to a note with no tags"""
    note = Note("Test note")
    original_updated_at = note.updated_at
    time.sleep(0.01)  # Small delay to ensure time difference

    note.add_tag("new_tag")

    assert "new_tag" in note.tags
    assert len(note.tags) == 1
    assert note.updated_at > original_updated_at


def test_add_tag_to_existing_tags():
    """Test adding a tag to a note with existing tags"""
    note = Note("Test note", ["tag1", "tag2"])

    note.add_tag("tag3")

    assert note.tags == ["tag1", "tag2", "tag3"]


def test_add_duplicate_tag():
    """Test that adding a duplicate tag doesn't create duplicates"""
    note = Note("Test note", ["tag1"])
    original_updated_at = note.updated_at
    time.sleep(0.01)

    note.add_tag("tag1")

    assert note.tags == ["tag1"]
    assert note.tags.count("tag1") == 1
    # updated_at should not change when duplicate tag is added
    assert note.updated_at == original_updated_at


def test_add_multiple_tags_sequentially():
    """Test adding multiple tags one by one"""
    note = Note("Test note")

    note.add_tag("tag1")
    note.add_tag("tag2")
    note.add_tag("tag3")

    assert note.tags == ["tag1", "tag2", "tag3"]


def test_add_tag_with_special_characters():
    """Test adding tags with special characters"""
    note = Note("Test note")

    note.add_tag("tag-with-dash")
    note.add_tag("tag_with_underscore")
    note.add_tag("tag.with.dot")

    assert len(note.tags) == 3
    assert "tag-with-dash" in note.tags


def test_add_empty_string_tag():
    """Test adding an empty string as tag"""
    note = Note("Test note")

    note.add_tag("")

    assert "" in note.tags


# Tests for remove_tag method

def test_remove_existing_tag():
    """Test removing an existing tag"""
    note = Note("Test note", ["tag1", "tag2", "tag3"])
    original_updated_at = note.updated_at
    time.sleep(0.01)

    note.remove_tag("tag2")

    assert note.tags == ["tag1", "tag3"]
    assert "tag2" not in note.tags
    assert note.updated_at > original_updated_at


def test_remove_non_existing_tag():
    """Test removing a tag that doesn't exist"""
    note = Note("Test note", ["tag1"])
    original_updated_at = note.updated_at
    original_tags = note.tags.copy()
    time.sleep(0.01)

    note.remove_tag("non_existing_tag")

    assert note.tags == original_tags
    # updated_at should not change when removing non-existing tag
    assert note.updated_at == original_updated_at


def test_remove_last_tag():
    """Test removing the last remaining tag"""
    note = Note("Test note", ["only_tag"])

    note.remove_tag("only_tag")

    assert note.tags == []


def test_remove_tag_from_empty_list():
    """Test removing a tag from a note with no tags"""
    note = Note("Test note")
    original_updated_at = note.updated_at

    note.remove_tag("any_tag")

    assert note.tags == []
    assert note.updated_at == original_updated_at


def test_remove_all_tags_sequentially():
    """Test removing all tags one by one"""
    note = Note("Test note", ["tag1", "tag2", "tag3"])

    note.remove_tag("tag1")
    note.remove_tag("tag2")
    note.remove_tag("tag3")

    assert note.tags == []


# Tests for edit_tags method

def test_edit_tags_with_new_list():
    """Test replacing tags with a new list"""
    note = Note("Test note", ["old1", "old2"])
    original_updated_at = note.updated_at
    time.sleep(0.01)

    note.edit_tags(["new1", "new2", "new3"])

    assert note.tags == ["new1", "new2", "new3"]
    assert note.updated_at > original_updated_at


def test_edit_tags_with_empty_list():
    """Test replacing tags with an empty list"""
    note = Note("Test note", ["tag1", "tag2"])

    note.edit_tags([])

    assert note.tags == []


def test_edit_tags_with_none():
    """Test replacing tags with None"""
    note = Note("Test note", ["tag1", "tag2"])

    note.edit_tags(None)

    assert note.tags == []


def test_edit_tags_from_empty_to_filled():
    """Test adding tags to a note with no tags using edit_tags"""
    note = Note("Test note")

    note.edit_tags(["new1", "new2"])

    assert note.tags == ["new1", "new2"]


def test_edit_tags_updates_timestamp():
    """Test that edit_tags updates the updated_at timestamp"""
    note = Note("Test note", ["tag1"])
    original_updated_at = note.updated_at
    time.sleep(0.01)

    note.edit_tags(["tag1"])  # Same tags

    assert note.updated_at > original_updated_at


def test_edit_tags_with_single_tag():
    """Test replacing tags with a single tag"""
    note = Note("Test note", ["tag1", "tag2", "tag3"])

    note.edit_tags(["single_tag"])

    assert note.tags == ["single_tag"]


# Tests for complex usage scenarios

def test_multiple_operations_on_note():
    """Test performing multiple operations on a single note"""
    note = Note("Complex note", ["initial"])

    note.add_tag("added1")
    note.add_tag("added2")
    note.remove_tag("initial")
    note.add_tag("added3")
    note.edit_tags(["final1", "final2"])

    assert note.tags == ["final1", "final2"]
    assert note.updated_at > note.created_at


def test_note_immutability_of_uuid():
    """Test that UUID doesn't change during note lifetime"""
    note = Note("Test note")
    original_uuid = note._uuid

    note.add_tag("tag1")
    note.remove_tag("tag1")
    note.edit_tags(["new_tag"])

    assert note._uuid == original_uuid


def test_timestamps_progression():
    """Test that updated_at progresses with operations"""
    note = Note("Test note")
    timestamp1 = note.updated_at

    time.sleep(0.01)
    note.add_tag("tag1")
    timestamp2 = note.updated_at

    time.sleep(0.01)
    note.add_tag("tag2")
    timestamp3 = note.updated_at

    assert timestamp1 < timestamp2 < timestamp3


def test_created_at_never_changes():
    """Test that created_at timestamp never changes"""
    note = Note("Test note")
    original_created_at = note.created_at

    time.sleep(0.01)
    note.add_tag("tag1")
    note.remove_tag("tag1")
    note.edit_tags(["new_tag"])

    assert note.created_at == original_created_at


def test_tags_list_independence():
    """Test that modifying the original tags list doesn't affect the note"""
    original_tags = ["tag1", "tag2"]
    note = Note("Test note", original_tags)

    original_tags.append("tag3")

    assert note.tags == ["tag1", "tag2"]
    assert "tag3" not in note.tags


# Tests for edge cases and boundary conditions

def test_very_long_text():
    """Test creating a note with very long text"""
    long_text = "a" * 10000
    note = Note(long_text)

    assert note.text == long_text
    assert len(note.text) == 10000


def test_text_with_special_characters():
    """Test creating a note with special characters in text"""
    special_text = "Note with 特殊字符 émojis 🎉🎊 and symbols !@#$%"
    note = Note(special_text)

    assert note.text == special_text


def test_text_with_newlines():
    """Test creating a note with newlines in text"""
    multiline_text = "Line 1\nLine 2\nLine 3"
    note = Note(multiline_text)

    assert note.text == multiline_text


def test_many_tags():
    """Test creating a note with many tags"""
    many_tags = [f"tag{i}" for i in range(100)]
    note = Note("Test note", many_tags)

    assert len(note.tags) == 100
    assert note.tags == many_tags


def test_tags_with_unicode():
    """Test tags with unicode characters"""
    note = Note("Test note")

    note.add_tag("тег")
    note.add_tag("标签")
    note.add_tag("🏷️")

    assert len(note.tags) == 3
    assert "тег" in note.tags
    assert "标签" in note.tags
    assert "🏷️" in note.tags


def test_text_with_only_one_character():
    """Test creating a note with single character"""
    note = Note("a")

    assert note.text == "a"


def test_whitespace_in_middle_of_text_is_valid():
    """Test that text with whitespace in the middle is valid"""
    note = Note("  Text with spaces  ")

    assert note.text == "  Text with spaces  "


# Tests for invalid input data and error handling

def test_init_with_integer_text():
    """Test that integer as text raises appropriate error"""
    with pytest.raises((ValueError, AttributeError)):
        Note(123)


def test_init_with_list_text():
    """Test that list as text raises appropriate error"""
    with pytest.raises((ValueError, AttributeError)):
        Note(["not", "a", "string"])


def test_init_with_dict_text():
    """Test that dict as text raises appropriate error"""
    with pytest.raises((ValueError, AttributeError)):
        Note({"text": "value"})


def test_init_with_boolean_false():
    """Test that boolean False as text raises ValueError"""
    with pytest.raises((ValueError, AttributeError)):
        Note(False)


def test_add_none_as_tag():
    """Test adding None as a tag"""
    note = Note("Test note")

    note.add_tag(None)

    assert None in note.tags


def test_add_number_as_tag():
    """Test adding a number as a tag"""
    note = Note("Test note")

    note.add_tag(123)

    assert 123 in note.tags


def test_remove_none_from_tags():
    """Test removing None from tags"""
    note = Note("Test note", [None, "tag1"])

    note.remove_tag(None)

    assert None not in note.tags
    assert note.tags == ["tag1"]


def test_edit_tags_with_tuple():
    """Test edit_tags with tuple"""
    note = Note("Test note", ["tag1"])

    note.edit_tags(("tuple_tag1", "tuple_tag2"))

    # Tuple is converted to list
    assert note.tags == ["tuple_tag1", "tuple_tag2"]


def test_edit_tags_with_tuple():
    """Test edit_tags with tuple"""
    note = Note("Test note", ["tag1"])

    note.edit_tags(("tuple_tag1", "tuple_tag2"))

    # Tuple is converted to list
    assert note.tags == ["tuple_tag1", "tuple_tag2"]
    assert isinstance(note.tags, list)


def test_add_tag_with_whitespace():
    """Test adding a tag with whitespace"""
    note = Note("Test note")

    note.add_tag("  tag with spaces  ")

    assert "  tag with spaces  " in note.tags


def test_remove_first_tag_from_multiple():
    """Test removing the first tag from multiple tags"""
    note = Note("Test note", ["first", "second", "third"])

    note.remove_tag("first")

    assert note.tags == ["second", "third"]


def test_remove_last_tag_from_multiple():
    """Test removing the last tag from multiple tags"""
    note = Note("Test note", ["first", "second", "third"])

    note.remove_tag("third")

    assert note.tags == ["first", "second"]


def test_str_with_long_text_and_many_tags():
    """Test string representation with long text and many tags"""
    long_text = "A" * 100
    many_tags = [f"tag{i}" for i in range(10)]
    note = Note(long_text, many_tags)

    result = str(note)

    assert long_text in result
    assert "Tags:" in result
    for tag in many_tags:
        assert tag in result


def test_uuid_format():
    """Test that UUID has correct format"""
    note = Note("Test note")
    uuid_parts = note._uuid.split('-')

    assert len(uuid_parts) == 5
    assert len(uuid_parts[0]) == 8
    assert len(uuid_parts[1]) == 4
    assert len(uuid_parts[2]) == 4
    assert len(uuid_parts[3]) == 4
    assert len(uuid_parts[4]) == 12


def test_multiple_notes_independent():
    """Test that multiple notes are independent"""
    note1 = Note("Note 1", ["tag1"])
    note2 = Note("Note 2", ["tag2"])

    note1.add_tag("shared_tag")

    assert "shared_tag" in note1.tags
    assert "shared_tag" not in note2.tags
    assert note1.text != note2.text


def test_tags_order_preserved():
    """Test that tags order is preserved"""
    note = Note("Test note")

    note.add_tag("zebra")
    note.add_tag("apple")
    note.add_tag("middle")

    assert note.tags == ["zebra", "apple", "middle"]


def test_edit_tags_replaces_completely():
    """Test that edit_tags completely replaces old tags"""
    note = Note("Test note", ["old1", "old2", "old3"])

    note.edit_tags(["new1"])

    assert "old1" not in note.tags
    assert "old2" not in note.tags
    assert "old3" not in note.tags
    assert note.tags == ["new1"]
