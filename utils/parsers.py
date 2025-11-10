import shlex
from difflib import get_close_matches
from core.commands import Command


def parse_input(input_string):
    """
    Parses user input into command and arguments, handling quoted strings
    """
    if len(input_string.strip()) == 0:
        return ("",)

    parts = shlex.split(input_string)

    cmd = ""
    if len(parts) == 0:
        return ("",)

    if len(parts) > 0:
        cmd = parts[0]
        cmd = cmd.strip().lower()

    arguments = parts[1:]

    return cmd, *arguments


def detect_command(user_command):
    """
    Detects and returns the command from user input,
    with auto-correction.
    """

    is_command_found = False
    for cmd in Command:
        if cmd.value == user_command:
            is_command_found = True
            break

    if is_command_found:
        return (user_command, True)

    if suggestions := get_close_matches(user_command, Command, n=3, cutoff=0.6):
        if suggestions and len(suggestions) == 1:
            print(f"It seems you've meant: '{suggestions[0]}' command. Apply auto-correction.")
            return (suggestions[0], True)
        else:
            print(f"Unknown command '{user_command}'. Did you mean: {', '.join(suggestions)}?")
            return (None, False)
    else:
        print(f"Unknown command '{user_command}'. Use '{Command.HELP}' to review available commands.")
        return (None, False)
