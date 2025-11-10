import pytest
import time

from models.note import Note
from models.notebook import NoteBook


# Tests for NoteBook initialization

def test_notebook_init():
    """Test creating a new notebook"""
    notebook = NoteBook()

    assert isinstance(notebook.notes, dict)
    assert len(notebook.notes) == 0
    assert len(notebook) == 0


def test_notebook_str():
    """Test string representation of notebook"""
    notebook = NoteBook()

    assert str(notebook) == "NoteBook with 0 note(s)"

    notebook.add_note(Note("Test"))
    assert str(notebook) == "NoteBook with 1 note(s)"

    notebook.add_note(Note("Test 2"))
    assert str(notebook) == "NoteBook with 2 note(s)"


# Tests for add_note method

def test_add_note_success():
    """Test adding a note successfully"""
    notebook = NoteBook()
    note = Note("Test note")

    result = notebook.add_note(note)

    assert result is True
    assert len(notebook) == 1
    assert note._uuid in notebook.notes
    assert notebook.notes[note._uuid] == note


def test_add_multiple_notes():
    """Test adding multiple notes"""
    notebook = NoteBook()
    note1 = Note("Note 1")
    note2 = Note("Note 2")
    note3 = Note("Note 3")

    notebook.add_note(note1)
    notebook.add_note(note2)
    notebook.add_note(note3)

    assert len(notebook) == 3
    assert note1._uuid in notebook.notes
    assert note2._uuid in notebook.notes
    assert note3._uuid in notebook.notes


def test_add_note_updates_existing():
    """Test that adding a note with existing UUID updates it"""
    notebook = NoteBook()
    note = Note("Original text", ["tag1"])

    # Add note first time
    result1 = notebook.add_note(note)
    assert result1 is True
    assert len(notebook) == 1

    # Modify note and add again (same UUID)
    note.text = "Modified text"
    note.add_tag("tag2")
    result2 = notebook.add_note(note)

    assert result2 is False  # Returns False because it's an update
    assert len(notebook) == 1  # Still only one note
    assert notebook.notes[note._uuid].text == "Modified text"
    assert "tag2" in notebook.notes[note._uuid].tags


def test_add_note_invalid_type_string():
    """Test adding a string instead of Note raises TypeError"""
    notebook = NoteBook()

    with pytest.raises(TypeError) as exc_info:
        notebook.add_note("not a note")

    assert "Only Note objects can be added" in str(exc_info.value)


def test_add_note_invalid_type_dict():
    """Test adding a dict instead of Note raises TypeError"""
    notebook = NoteBook()

    with pytest.raises(TypeError) as exc_info:
        notebook.add_note({"text": "note"})

    assert "Only Note objects can be added" in str(exc_info.value)


def test_add_note_invalid_type_none():
    """Test adding None raises TypeError"""
    notebook = NoteBook()

    with pytest.raises(TypeError) as exc_info:
        notebook.add_note(None)

    assert "Only Note objects can be added" in str(exc_info.value)


def test_add_note_invalid_type_number():
    """Test adding a number raises TypeError"""
    notebook = NoteBook()

    with pytest.raises(TypeError) as exc_info:
        notebook.add_note(123)

    assert "Only Note objects can be added" in str(exc_info.value)


# Tests for delete_note method

def test_delete_note_success():
    """Test deleting an existing note"""
    notebook = NoteBook()
    note = Note("Test note")
    notebook.add_note(note)

    result = notebook.delete_note(note._uuid)

    assert result is True
    assert len(notebook) == 0
    assert note._uuid not in notebook.notes


def test_delete_note_non_existing():
    """Test deleting a non-existing note returns False"""
    notebook = NoteBook()

    result = notebook.delete_note("non-existing-uuid")

    assert result is False
    assert len(notebook) == 0


def test_delete_note_from_multiple():
    """Test deleting one note from multiple"""
    notebook = NoteBook()
    note1 = Note("Note 1")
    note2 = Note("Note 2")
    note3 = Note("Note 3")

    notebook.add_note(note1)
    notebook.add_note(note2)
    notebook.add_note(note3)

    result = notebook.delete_note(note2._uuid)

    assert result is True
    assert len(notebook) == 2
    assert note1._uuid in notebook.notes
    assert note2._uuid not in notebook.notes
    assert note3._uuid in notebook.notes


def test_delete_all_notes():
    """Test deleting all notes one by one"""
    notebook = NoteBook()
    notes = [Note(f"Note {i}") for i in range(5)]

    for note in notes:
        notebook.add_note(note)

    for note in notes:
        result = notebook.delete_note(note._uuid)
        assert result is True

    assert len(notebook) == 0


def test_delete_note_with_invalid_id():
    """Test deleting with invalid UUID format"""
    notebook = NoteBook()
    note = Note("Test")
    notebook.add_note(note)

    result = notebook.delete_note("invalid-uuid-format")

    assert result is False
    assert len(notebook) == 1


# Tests for get_all_notes method

def test_get_all_notes_empty():
    """Test getting all notes from empty notebook"""
    notebook = NoteBook()

    notes = notebook.get_all_notes()

    assert notes == []
    assert isinstance(notes, list)


def test_get_all_notes_default_sort():
    """Test getting all notes with default sorting (created)"""
    notebook = NoteBook()
    note1 = Note("First note")
    time.sleep(0.01)
    note2 = Note("Second note")
    time.sleep(0.01)
    note3 = Note("Third note")

    notebook.add_note(note1)
    notebook.add_note(note2)
    notebook.add_note(note3)

    notes = notebook.get_all_notes()

    assert len(notes) == 3
    # Newer notes first
    assert notes[0] == note3
    assert notes[1] == note2
    assert notes[2] == note1


def test_get_all_notes_sort_by_created():
    """Test sorting by created date"""
    notebook = NoteBook()
    note1 = Note("First")
    time.sleep(0.01)
    note2 = Note("Second")
    time.sleep(0.01)
    note3 = Note("Third")

    notebook.add_note(note1)
    notebook.add_note(note2)
    notebook.add_note(note3)

    notes = notebook.get_all_notes(sort_by="created")

    assert notes[0] == note3  # Newest first
    assert notes[1] == note2
    assert notes[2] == note1


def test_get_all_notes_sort_by_updated():
    """Test sorting by updated date"""
    notebook = NoteBook()
    note1 = Note("First")
    note2 = Note("Second")
    note3 = Note("Third")

    notebook.add_note(note1)
    notebook.add_note(note2)
    notebook.add_note(note3)

    time.sleep(0.01)
    note1.add_tag("updated")  # This updates note1

    notes = notebook.get_all_notes(sort_by="updated")

    assert notes[0] == note1  # Most recently updated first


def test_get_all_notes_sort_by_text():
    """Test sorting by text alphabetically"""
    notebook = NoteBook()
    note1 = Note("Zebra")
    note2 = Note("Apple")
    note3 = Note("Mango")

    notebook.add_note(note1)
    notebook.add_note(note2)
    notebook.add_note(note3)

    notes = notebook.get_all_notes(sort_by="text", reverse=False)

    assert notes[0] == note2  # Apple
    assert notes[1] == note3  # Mango
    assert notes[2] == note1  # Zebra


def test_get_all_notes_sort_by_text_case_insensitive():
    """Test that text sorting is case-insensitive"""
    notebook = NoteBook()
    note1 = Note("banana")
    note2 = Note("Apple")
    note3 = Note("CHERRY")

    notebook.add_note(note1)
    notebook.add_note(note2)
    notebook.add_note(note3)

    notes = notebook.get_all_notes(sort_by="text", reverse=False)

    assert notes[0].text == "Apple"
    assert notes[1].text == "banana"
    assert notes[2].text == "CHERRY"


def test_get_all_notes_sort_by_tags():
    """Test sorting by tags alphabetically"""
    notebook = NoteBook()
    note1 = Note("Note 1", ["zebra"])
    note2 = Note("Note 2", ["apple"])
    note3 = Note("Note 3", ["mango"])

    notebook.add_note(note1)
    notebook.add_note(note2)
    notebook.add_note(note3)

    notes = notebook.get_all_notes(sort_by="tags", reverse=False)

    assert notes[0] == note2  # apple
    assert notes[1] == note3  # mango
    assert notes[2] == note1  # zebra


def test_get_all_notes_sort_by_tags_with_no_tags():
    """Test sorting by tags when some notes have no tags"""
    notebook = NoteBook()
    note1 = Note("Note with tag", ["apple"])
    note2 = Note("Note without tags")
    note3 = Note("Another tagged", ["zebra"])

    notebook.add_note(note1)
    notebook.add_note(note2)
    notebook.add_note(note3)

    notes = notebook.get_all_notes(sort_by="tags", reverse=False)

    # Notes with tags come first, sorted alphabetically
    # Notes without tags come last
    assert notes[0] == note1  # apple
    assert notes[1] == note3  # zebra
    assert notes[2] == note2  # no tags


def test_get_all_notes_sort_invalid_method():
    """Test that invalid sort method defaults to 'created'"""
    notebook = NoteBook()
    note1 = Note("First")
    time.sleep(0.01)
    note2 = Note("Second")

    notebook.add_note(note1)
    notebook.add_note(note2)

    notes = notebook.get_all_notes(sort_by="invalid_sort")

    # Should default to created (newer first)
    assert notes[0] == note2
    assert notes[1] == note1


# Tests for get_note_by_number method

def test_get_note_by_number_first():
    """Test getting the first note"""
    notebook = NoteBook()
    note1 = Note("First")
    note2 = Note("Second")

    notebook.add_note(note1)
    notebook.add_note(note2)

    result = notebook.get_note_by_number(1, sort_by="text")

    assert result == note1


def test_get_note_by_number_last():
    """Test getting the last note"""
    notebook = NoteBook()
    notes = [Note(f"Note {i}") for i in range(5)]

    for note in notes:
        notebook.add_note(note)

    result = notebook.get_note_by_number(5, sort_by="text")

    assert result is not None


def test_get_note_by_number_middle():
    """Test getting a middle note"""
    notebook = NoteBook()
    note1 = Note("Apple")
    note2 = Note("Banana")
    note3 = Note("Cherry")

    notebook.add_note(note1)
    notebook.add_note(note2)
    notebook.add_note(note3)

    result = notebook.get_note_by_number(2, sort_by="text")

    assert result == note2


def test_get_note_by_number_out_of_range():
    """Test getting note with out of range number returns None"""
    notebook = NoteBook()
    notebook.add_note(Note("Test"))

    result = notebook.get_note_by_number(10)

    assert result is None


def test_get_note_by_number_zero():
    """Test that number 0 returns None"""
    notebook = NoteBook()
    notebook.add_note(Note("Test"))

    result = notebook.get_note_by_number(0)

    assert result is None


def test_get_note_by_number_negative():
    """Test that negative number returns None"""
    notebook = NoteBook()
    notebook.add_note(Note("Test"))

    result = notebook.get_note_by_number(-1)

    assert result is None


def test_get_note_by_number_empty_notebook():
    """Test getting note from empty notebook returns None"""
    notebook = NoteBook()

    result = notebook.get_note_by_number(1)

    assert result is None


def test_get_note_by_number_with_different_sort():
    """Test getting note with different sorting methods"""
    notebook = NoteBook()
    note1 = Note("Zebra", ["alpha"])
    time.sleep(0.01)
    note2 = Note("Apple", ["zulu"])

    notebook.add_note(note1)
    notebook.add_note(note2)

    by_text = notebook.get_note_by_number(1, sort_by="text")
    by_tags = notebook.get_note_by_number(1, sort_by="tags")
    by_created = notebook.get_note_by_number(1, sort_by="created")

    assert by_text == note2  # Apple comes first alphabetically
    assert by_tags == note1  # alpha comes first
    assert by_created == note2  # note2 was created last


# Tests for get_note_id_by_number method

def test_get_note_id_by_number_success():
    """Test getting note ID by number"""
    notebook = NoteBook()
    note = Note("Test")
    notebook.add_note(note)

    note_id = notebook.get_note_id_by_number(1)

    assert note_id == note._uuid


def test_get_note_id_by_number_none():
    """Test getting note ID with invalid number returns None"""
    notebook = NoteBook()
    notebook.add_note(Note("Test"))

    note_id = notebook.get_note_id_by_number(10)

    assert note_id is None


def test_get_note_id_by_number_empty_notebook():
    """Test getting note ID from empty notebook returns None"""
    notebook = NoteBook()

    note_id = notebook.get_note_id_by_number(1)

    assert note_id is None


def test_get_note_id_by_number_with_sort():
    """Test getting note ID with different sorting"""
    notebook = NoteBook()
    note1 = Note("Zebra")
    note2 = Note("Apple")

    notebook.add_note(note1)
    notebook.add_note(note2)

    id_by_text = notebook.get_note_id_by_number(1, sort_by="text")

    assert id_by_text == note2._uuid  # Apple is first alphabetically


# Tests for find_note_by_text method

def test_find_note_by_text_found():
    """Test finding a note by text fragment"""
    notebook = NoteBook()
    note1 = Note("Buy groceries")
    note2 = Note("Call mom")

    notebook.add_note(note1)
    notebook.add_note(note2)

    result = notebook.find_note_by_text("groceries")

    assert result == note1


def test_find_note_by_text_case_insensitive():
    """Test that text search is case-insensitive"""
    notebook = NoteBook()
    note = Note("BUY GROCERIES")
    notebook.add_note(note)

    result = notebook.find_note_by_text("groceries")

    assert result == note


def test_find_note_by_text_partial_match():
    """Test finding note with partial text match"""
    notebook = NoteBook()
    note = Note("Important meeting tomorrow")
    notebook.add_note(note)

    result = notebook.find_note_by_text("meeting")

    assert result == note


def test_find_note_by_text_not_found():
    """Test that searching for non-existing text returns None"""
    notebook = NoteBook()
    notebook.add_note(Note("Test note"))

    result = notebook.find_note_by_text("non-existing")

    assert result is None


def test_find_note_by_text_empty_notebook():
    """Test searching in empty notebook returns None"""
    notebook = NoteBook()

    result = notebook.find_note_by_text("anything")

    assert result is None


def test_find_note_by_text_returns_first():
    """Test that only the first matching note is returned"""
    notebook = NoteBook()
    note1 = Note("First test note")
    note2 = Note("Second test note")

    notebook.add_note(note1)
    notebook.add_note(note2)

    result = notebook.find_note_by_text("test")

    assert result in [note1, note2]
    # Should return only one note, not both


def test_find_note_by_text_empty_string():
    """Test finding note with empty string"""
    notebook = NoteBook()
    note = Note("Test note")
    notebook.add_note(note)

    result = notebook.find_note_by_text("")

    assert result == note  # Empty string is in every string


# Tests for search_notes method

def test_search_notes_by_text():
    """Test searching notes by text"""
    notebook = NoteBook()
    note1 = Note("Buy groceries")
    note2 = Note("Buy tickets")
    note3 = Note("Call mom")

    notebook.add_note(note1)
    notebook.add_note(note2)
    notebook.add_note(note3)

    results = notebook.search_notes("buy")

    assert len(results) == 2
    assert note1 in results
    assert note2 in results
    assert note3 not in results


def test_search_notes_by_tag():
    """Test searching notes by tag"""
    notebook = NoteBook()
    note1 = Note("Note 1", ["important"])
    note2 = Note("Note 2", ["urgent"])
    note3 = Note("Note 3", ["important"])

    notebook.add_note(note1)
    notebook.add_note(note2)
    notebook.add_note(note3)

    results = notebook.search_notes("important")

    assert len(results) == 2
    assert note1 in results
    assert note3 in results


def test_search_notes_case_insensitive():
    """Test that search is case-insensitive"""
    notebook = NoteBook()
    note1 = Note("IMPORTANT NOTE", ["URGENT"])
    note2 = Note("regular note", ["normal"])

    notebook.add_note(note1)
    notebook.add_note(note2)

    results = notebook.search_notes("important")

    assert len(results) == 1
    assert note1 in results


def test_search_notes_no_results():
    """Test searching with no matching results"""
    notebook = NoteBook()
    notebook.add_note(Note("Test note"))

    results = notebook.search_notes("non-existing")

    assert results == []


def test_search_notes_empty_notebook():
    """Test searching in empty notebook"""
    notebook = NoteBook()

    results = notebook.search_notes("anything")

    assert results == []


def test_search_notes_partial_match():
    """Test searching with partial text match"""
    notebook = NoteBook()
    note = Note("Meeting tomorrow at 3pm")
    notebook.add_note(note)

    results = notebook.search_notes("tomorrow")

    assert len(results) == 1
    assert note in results


def test_search_notes_matches_text_not_tag():
    """Test that note is added only once even if it matches both text and tag"""
    notebook = NoteBook()
    note = Note("Important task", ["important"])
    notebook.add_note(note)

    results = notebook.search_notes("important")

    assert len(results) == 1
    assert results.count(note) == 1


def test_search_notes_empty_query():
    """Test searching with empty query"""
    notebook = NoteBook()
    note1 = Note("Note 1")
    note2 = Note("Note 2")

    notebook.add_note(note1)
    notebook.add_note(note2)

    results = notebook.search_notes("")

    # Empty string is in every string
    assert len(results) == 2


def test_search_notes_with_special_characters():
    """Test searching with special characters"""
    notebook = NoteBook()
    note = Note("Price is $100")
    notebook.add_note(note)

    results = notebook.search_notes("$100")

    assert len(results) == 1
    assert note in results


# Tests for search_by_tags method

def test_search_by_tags_single_tag():
    """Test searching by single tag"""
    notebook = NoteBook()
    note1 = Note("Note 1", ["important"])
    note2 = Note("Note 2", ["urgent"])
    note3 = Note("Note 3", ["important"])

    notebook.add_note(note1)
    notebook.add_note(note2)
    notebook.add_note(note3)

    results = notebook.search_by_tags(["important"])

    assert len(results) == 2
    assert note1 in results
    assert note3 in results


def test_search_by_tags_multiple_tags_all_present():
    """Test searching by multiple tags - all must be present"""
    notebook = NoteBook()
    note1 = Note("Note 1", ["important", "work"])
    note2 = Note("Note 2", ["important", "personal"])
    note3 = Note("Note 3", ["important", "work", "urgent"])

    notebook.add_note(note1)
    notebook.add_note(note2)
    notebook.add_note(note3)

    results = notebook.search_by_tags(["important", "work"])

    assert len(results) == 2
    assert note1 in results
    assert note3 in results
    assert note2 not in results


def test_search_by_tags_no_matches():
    """Test searching by tags with no matches"""
    notebook = NoteBook()
    note = Note("Note", ["tag1", "tag2"])
    notebook.add_note(note)

    results = notebook.search_by_tags(["tag3"])

    assert results == []


def test_search_by_tags_empty_list():
    """Test searching with empty tags list returns empty list"""
    notebook = NoteBook()
    notebook.add_note(Note("Note", ["tag1"]))

    results = notebook.search_by_tags([])

    assert results == []


def test_search_by_tags_case_insensitive():
    """Test that tag search is case-insensitive"""
    notebook = NoteBook()
    note = Note("Note", ["IMPORTANT", "WORK"])
    notebook.add_note(note)

    results = notebook.search_by_tags(["important", "work"])

    assert len(results) == 1
    assert note in results


def test_search_by_tags_partial_match_not_found():
    """Test that partial tag matches don't count"""
    notebook = NoteBook()
    note = Note("Note", ["important", "work"])
    notebook.add_note(note)

    results = notebook.search_by_tags(["import"])  # Partial match

    assert results == []


def test_search_by_tags_note_without_tags():
    """Test that notes without tags are not found"""
    notebook = NoteBook()
    note = Note("Note without tags")
    notebook.add_note(note)

    results = notebook.search_by_tags(["any_tag"])

    assert results == []


def test_search_by_tags_empty_notebook():
    """Test searching in empty notebook"""
    notebook = NoteBook()

    results = notebook.search_by_tags(["tag"])

    assert results == []


def test_search_by_tags_with_none_tag():
    """Test searching with None in tags list"""
    notebook = NoteBook()
    note = Note("Note", [None, "tag1"])
    notebook.add_note(note)

    results = notebook.search_by_tags([None])

    assert len(results) == 1
    assert note in results


def test_search_by_tags_with_number_tag():
    """Test searching with numeric tags"""
    notebook = NoteBook()
    note = Note("Note", [123, "tag1"])
    notebook.add_note(note)

    results = notebook.search_by_tags([123])

    assert len(results) == 1
    assert note in results


# Tests for complex scenarios

def test_notebook_full_workflow():
    """Test complete workflow with multiple operations"""
    notebook = NoteBook()

    # Add notes
    note1 = Note("Buy groceries", ["shopping", "important"])
    note2 = Note("Call dentist", ["health", "urgent"])
    note3 = Note("Finish report", ["work", "important"])

    notebook.add_note(note1)
    notebook.add_note(note2)
    notebook.add_note(note3)

    assert len(notebook) == 3

    # Search
    important_notes = notebook.search_by_tags(["important"])
    assert len(important_notes) == 2

    # Get by number
    first_note = notebook.get_note_by_number(1, sort_by="text")
    assert first_note is not None

    # Delete
    deleted = notebook.delete_note(note2._uuid)
    assert deleted is True
    assert len(notebook) == 2

    # Search again
    all_notes = notebook.get_all_notes()
    assert len(all_notes) == 2


def test_notebook_with_many_notes():
    """Test notebook with many notes"""
    notebook = NoteBook()
    notes = [Note(f"Note {i}", [f"tag{i % 5}"]) for i in range(100)]

    for note in notes:
        notebook.add_note(note)

    assert len(notebook) == 100

    all_notes = notebook.get_all_notes()
    assert len(all_notes) == 100

    # Search by tag
    results = notebook.search_by_tags(["tag0"])
    assert len(results) == 20


def test_notebook_sorting_stability():
    """Test that sorting is stable across multiple calls"""
    notebook = NoteBook()
    note1 = Note("Apple")
    note2 = Note("Banana")
    note3 = Note("Cherry")

    notebook.add_note(note1)
    notebook.add_note(note2)
    notebook.add_note(note3)

    sorted1 = notebook.get_all_notes(sort_by="text")
    sorted2 = notebook.get_all_notes(sort_by="text")

    assert sorted1 == sorted2


def test_notebook_operations_independence():
    """Test that operations don't affect original note objects incorrectly"""
    notebook = NoteBook()
    note = Note("Original", ["tag1"])
    original_text = note.text
    original_tags = note.tags.copy()

    notebook.add_note(note)

    # Operations on notebook shouldn't affect the note
    notebook.get_all_notes()
    notebook.search_notes("original")

    assert note.text == original_text
    assert note.tags == original_tags


def test_multiple_notebooks_independence():
    """Test that multiple notebooks are independent"""
    notebook1 = NoteBook()
    notebook2 = NoteBook()

    note1 = Note("Notebook 1 note")
    note2 = Note("Notebook 2 note")

    notebook1.add_note(note1)
    notebook2.add_note(note2)

    assert len(notebook1) == 1
    assert len(notebook2) == 1
    assert note1._uuid in notebook1.notes
    assert note1._uuid not in notebook2.notes
    assert note2._uuid in notebook2.notes
    assert note2._uuid not in notebook1.notes


def test_notebook_len_after_operations():
    """Test that __len__ stays accurate after various operations"""
    notebook = NoteBook()

    assert len(notebook) == 0

    note1 = Note("Note 1")
    notebook.add_note(note1)
    assert len(notebook) == 1

    note2 = Note("Note 2")
    notebook.add_note(note2)
    assert len(notebook) == 2

    notebook.delete_note(note1._uuid)
    assert len(notebook) == 1

    notebook.delete_note(note2._uuid)
    assert len(notebook) == 0


def test_search_with_unicode_characters():
    """Test searching with unicode characters"""
    notebook = NoteBook()
    note1 = Note("Привіт світ", ["тег"])
    note2 = Note("Hello world", ["tag"])

    notebook.add_note(note1)
    notebook.add_note(note2)

    results = notebook.search_notes("світ")
    assert len(results) == 1
    assert note1 in results

    tag_results = notebook.search_by_tags(["тег"])
    assert len(tag_results) == 1
    assert note1 in tag_results


def test_sorting_with_identical_values():
    """Test sorting when multiple notes have identical sort values"""
    notebook = NoteBook()
    note1 = Note("Same text")
    note2 = Note("Same text")
    note3 = Note("Same text")

    notebook.add_note(note1)
    notebook.add_note(note2)
    notebook.add_note(note3)

    sorted_notes = notebook.get_all_notes(sort_by="text")

    assert len(sorted_notes) == 3
    # All three notes should be present
    assert note1 in sorted_notes
    assert note2 in sorted_notes
    assert note3 in sorted_notes
