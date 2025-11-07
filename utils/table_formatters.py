"""
Simple table formatters using tabulate.
"""
# flake8: noqa: E501
from tabulate import tabulate
from colorama import Fore, Style


def format_contact_table(records):
    """
    Format contacts as a simple table.
    
    Args:
        records: List of Record objects
        
    Returns:
        str: Formatted table string
    """
    if not records:
        return f"{Fore.YELLOW}No contacts found.{Style.RESET_ALL}"

    headers = [
        f"{Fore.CYAN}Name{Style.RESET_ALL}",
        f"{Fore.GREEN}Phones{Style.RESET_ALL}",
        f"{Fore.YELLOW}Email{Style.RESET_ALL}",
        f"{Fore.MAGENTA}Birthday{Style.RESET_ALL}"
    ]
    table_data = []

    for record in records:
        name = f"{Fore.CYAN}{record.name.value}{Style.RESET_ALL}"
        phones = f"{Fore.GREEN}{'; '.join(p.value for p in record.phones)}{Style.RESET_ALL}" if record.phones else f"{Fore.WHITE}-{Style.RESET_ALL}"
        email = f"{Fore.YELLOW}{record.email.value}{Style.RESET_ALL}" if record.email else f"{Fore.WHITE}-{Style.RESET_ALL}"
        birthday = f"{Fore.MAGENTA}{str(record.birthday)}{Style.RESET_ALL}" if record.birthday else f"{Fore.WHITE}-{Style.RESET_ALL}"

        table_data.append([name, phones, email, birthday])

    return tabulate(table_data, headers=headers, tablefmt="rounded_outline")


def format_notes_table(notes):
    """
    Format notes as a simple table.
    
    Args:
        notes: List of Note objects
        
    Returns:
        str: Formatted table string
    """
    if not notes:
        return f"{Fore.YELLOW}No notes found.{Style.RESET_ALL}"

    headers = [
        f"{Fore.GREEN}#{Style.RESET_ALL}",
        f"{Fore.WHITE}Text{Style.RESET_ALL}",
        f"{Fore.CYAN}Tags{Style.RESET_ALL}",
        f"{Fore.BLUE}Created{Style.RESET_ALL}",
        f"{Fore.MAGENTA}Updated{Style.RESET_ALL}"
    ]
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
