"""
Input enhancement utilities for the CLI application.

This module provides readline support for command history and tab completion.
"""

import os
import atexit

# Try to import readline at module level
try:
    import readline  # noqa: F401
    READLINE_AVAILABLE = True
    READLINE_MODULE = readline
except ImportError:
    # Try gnureadline for macOS
    try:
        import gnureadline as readline  # noqa: F401
        READLINE_AVAILABLE = True
        READLINE_MODULE = readline
    except ImportError:
        # No readline support available
        READLINE_AVAILABLE = False
        READLINE_MODULE = None


def setup_readline(commands):
    """
    Initialize readline for command history and tab completion.

    Args:
        commands: Command enum or list of command strings

    Returns:
        bool: True if readline was successfully initialized, False otherwise
    """
    if not READLINE_AVAILABLE or READLINE_MODULE is None:
        return False

    readline_module = READLINE_MODULE

    # Get command values
    try:
        # If it's an enum or class with .value attribute
        command_values = [cmd.value for cmd in commands]
    except (AttributeError, TypeError):
        # If it's already a list of strings
        command_values = list(commands) if commands else []

    # Enable history file
    histfile = os.path.join(os.path.expanduser("~"), ".addressbook_history")
    try:
        readline_module.read_history_file(histfile)
    except (FileNotFoundError, OSError):
        pass

    # Set history length
    readline_module.set_history_length(1000)

    # Save history on exit
    atexit.register(readline_module.write_history_file, histfile)

    # Setup tab completion
    def command_completer(text, state):
        """Tab completion function for commands."""
        try:
            matches = [cmd for cmd in command_values if cmd.startswith(text)]
            if state < len(matches):
                return matches[state]
            return None
        except (AttributeError, TypeError, IndexError):
            return None

    readline_module.set_completer(command_completer)
    readline_module.parse_and_bind("tab: complete")

    return True
