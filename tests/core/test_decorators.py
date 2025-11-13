"""
Tests for the decorators module.

This module contains tests for the input_error decorator functionality.
"""

from core.decorators import input_error


def test_input_error_handles_value_error():
    """Test that input_error decorator handles ValueError correctly."""

    @input_error
    def test_func():
        raise ValueError("Test error")

    result = test_func()
    assert "Error: Test error" in result


def test_input_error_handles_key_error():
    """Test that input_error decorator handles KeyError correctly."""

    @input_error
    def test_func():
        raise KeyError("Test error")

    result = test_func()
    assert result == "Contact not found"


def test_input_error_handles_index_error():
    """Test that input_error decorator handles IndexError correctly."""

    @input_error
    def test_func():
        raise IndexError("Test error")

    result = test_func()
    assert result == "Enter the argument for the command"


def test_input_error_handles_attribute_error():
    """Test that input_error decorator handles AttributeError correctly."""

    @input_error
    def test_func():
        raise AttributeError("Test error")

    result = test_func()
    assert result == "Contact not found"


def test_input_error_passes_through_normal_result():
    """Test that input_error decorator passes through normal results."""

    @input_error
    def test_func():
        return "Success"

    result = test_func()
    assert result == "Success"


def test_input_error_passes_through_with_args():
    """Test that input_error decorator works with function arguments."""

    @input_error
    def test_func(x, y):
        return x + y

    result = test_func(2, 3)
    assert result == 5


def test_input_error_preserves_function_metadata():
    """Test that input_error decorator preserves function metadata."""

    @input_error
    def test_func():
        """Test function docstring."""
        pass

    assert test_func.__name__ == "test_func"
    assert "Test function docstring" in test_func.__doc__


def test_input_error_unhandled_exception():
    """Test that unhandled exceptions are propagated."""

    @input_error
    def test_func():
        raise RuntimeError("Unhandled error")

    try:
        test_func()
        assert False, "Expected RuntimeError to be raised"
    except RuntimeError as e:
        assert "Unhandled error" in str(e)
