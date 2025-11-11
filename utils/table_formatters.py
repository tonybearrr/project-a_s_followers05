"""
Simple table formatters using tabulate.
"""
# flake8: noqa: E501
import re
from tabulate import tabulate
from colorama import Fore, Style, Back


def format_contact_table(records, value=None):
    """
    Format contacts as a simple table.
    
    Args:
        records: List of Record objects
        
    Returns:
        str: Formatted table string
    """
    if not records:
        return f"{Fore.YELLOW}No contacts found.{Style.RESET_ALL}"

    pattern = r"(\d{3})(\d{3})(\d{4})"
    replacement = r"(\1)\2-\3"
    # formatted_phone = re.sub(pattern, replacement, phone)
    headers = [
        f"{Fore.CYAN}Name{Style.RESET_ALL}",
        f"{Fore.GREEN}Phones{Style.RESET_ALL}",
        f"{Fore.YELLOW}Email{Style.RESET_ALL}",
        f"{Fore.MAGENTA}Birthday{Style.RESET_ALL}"
    ]
    table_data = []

    for record in records:
        if value:
            if value in record.name.value:
                match = re.search(value.lower(), record.name.value.lower())
                if match:
                    value_position = match.span()
                    part1 = f"{Fore.CYAN}{record.name.value[:value_position[0]]}{Style.RESET_ALL}"
                    part2 = f"{Fore.CYAN}{record.name.value[value_position[1]:]}{Style.RESET_ALL}"
                    value_hightligted = f"{Style.RESET_ALL}{Style.BRIGHT}{Fore.BLUE}{Back.LIGHTWHITE_EX}{value}{Style.RESET_ALL}"
                    
                    name = part1 + value_hightligted + part2
            else:
                name = f"{Fore.CYAN}{record.name.value}{Style.RESET_ALL}"

            phones = f"{Fore.GREEN}{' | '.join((re.sub(pattern, replacement, p.value)) for p in record.phones)}{Style.RESET_ALL}" if record.phones else f"{Fore.WHITE}-{Style.RESET_ALL}"
            # phones = f"{Fore.GREEN}{' | '.join(p.value for p in record.phones)}{Style.RESET_ALL}" if record.phones else f"{Fore.WHITE}-{Style.RESET_ALL}"

            if record.email: 
                if value in record.email.value:
                    match = re.search(value.lower(), record.email.value.lower())
                    if match:
                        value_position = match.span()
                        part1 = f"{Fore.YELLOW}{record.email.value[:value_position[0]]}{Style.RESET_ALL}"
                        part2 = f"{Fore.YELLOW}{record.email.value[value_position[1]:]}{Style.RESET_ALL}"
                        value_hightligted = f"{Style.RESET_ALL}{Style.BRIGHT}{Fore.YELLOW}{Back.LIGHTWHITE_EX}{value}{Style.RESET_ALL}"

                        email = part1 + value_hightligted + part2
                else:
                    email = f"{Fore.YELLOW}{record.email.value}{Style.RESET_ALL}"
                        
            else:
                email = f"{Fore.WHITE}-{Style.RESET_ALL}"

            birthday = f"{Fore.MAGENTA}{str(record.birthday)}{Style.RESET_ALL}" if record.birthday else f"{Fore.WHITE}-{Style.RESET_ALL}"

        else:
            name = f"{Fore.CYAN}{record.name.value}{Style.RESET_ALL}"
            phones = f"{Fore.GREEN}{' | '.join((re.sub(pattern, replacement, p.value)) for p in record.phones)}{Style.RESET_ALL}" if record.phones else f"{Fore.WHITE}-{Style.RESET_ALL}"
            # phones = f"{Fore.GREEN}{' | '.join(p.value for p in record.phones)}{Style.RESET_ALL}" if record.phones else f"{Fore.WHITE}-{Style.RESET_ALL}"
            email = f"{Fore.YELLOW}{record.email.value}{Style.RESET_ALL}" if record.email else f"{Fore.WHITE}-{Style.RESET_ALL}"
            birthday = f"{Fore.MAGENTA}{str(record.birthday)}{Style.RESET_ALL}" if record.birthday else f"{Fore.WHITE}-{Style.RESET_ALL}"

        table_data.append([name, phones, email, birthday])

    return tabulate(table_data, headers=headers, tablefmt="rounded_outline")


def format_notes_table(notes, sort_by=None, reverse=True):
    """
    Format notes as a simple table.
    
    Args:
        notes: List of Note objects
        sort_by: Optional sort column name (created, updated, text, tags)
        reverse: Sort direction (True for descending ↓, False for ascending ↑)
        
    Returns:
        str: Formatted table string
    """
    if not notes:
        return f"{Fore.YELLOW}No notes found.{Style.RESET_ALL}"

    # Define column headers with colors
    column_configs = [
        {"name": "#", "color": Fore.GREEN},
        {"name": "Text", "color": Fore.WHITE, "sort_key": "text"},
        {"name": "Tags", "color": Fore.CYAN, "sort_key": "tags"},
        {"name": "Created", "color": Fore.BLUE, "sort_key": "created"},
        {"name": "Updated", "color": Fore.MAGENTA, "sort_key": "updated"},
    ]

    # Build headers with sort indicator
    # Use bold Unicode characters for better visibility
    sort_indicator = "⏷" if reverse else "⏶"  # ⬇ and ⬆ are bolder than ↓ and ↑
    headers = []
    for col in column_configs:
        if col.get("sort_key") == sort_by:
            header = f"{col['color']}{col['name']}{Style.RESET_ALL} {Fore.YELLOW}{Style.BRIGHT}{sort_indicator}{Style.RESET_ALL}"
        else:
            header = f"{col['color']}{col['name']}{Style.RESET_ALL}"
        headers.append(header)
    table_data = []

    for i, note in enumerate(notes, 1):
        text = note.text[:47] + "..." if len(note.text) > 50 else note.text
        tags = ", ".join(note.tags) if note.tags else "-"
        created = note.created_at.strftime("%Y-%m-%d %H:%M") if hasattr(note.created_at, 'strftime') else str(note.created_at)
        updated = note.updated_at.strftime("%Y-%m-%d %H:%M") if hasattr(note.updated_at, 'strftime') else str(note.updated_at)

        num = f"{Fore.GREEN}{i}{Style.RESET_ALL}"
        text_colored = f"{Fore.WHITE}{text}{Style.RESET_ALL}"
        tags_colored = f"{Fore.CYAN}{tags}{Style.RESET_ALL}" if note.tags else f"{Fore.WHITE}-{Style.RESET_ALL}"
        created_colored = f"{Fore.BLUE}{created}{Style.RESET_ALL}"
        updated_colored = f"{Fore.MAGENTA}{updated}{Style.RESET_ALL}"

        table_data.append([num, text_colored, tags_colored, created_colored, updated_colored])

    return tabulate(table_data, headers=headers, tablefmt="rounded_outline")
