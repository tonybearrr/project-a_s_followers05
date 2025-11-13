"""
Help formatter with categories and examples.
"""
# flake8: noqa: E501
from colorama import Fore, Style, init
from core.commands import Command
from models.phone import Phone
from models.birthday import Birthday

init(autoreset=True)

# Formatting constants
LINE_WIDTH = 70
DOUBLE_LINE = "═" * LINE_WIDTH
SINGLE_LINE = "─" * LINE_WIDTH


def _header_line(color=Fore.CYAN, char="═"):
    """Generate a header line with specified color and character."""
    return f"{color}{char * LINE_WIDTH}{Style.RESET_ALL}"


def _section_line(color=Fore.YELLOW, char="─"):
    """Generate a section separator line with specified color and character."""
    return f"{color}{char * LINE_WIDTH}{Style.RESET_ALL}"


def format_help_full():
    """
    Format full help with categories and examples.
    
    Returns:
        str: Formatted help text
    """
    help_text = []

    # Header
    help_text.append(_header_line())
    help_text.append(f"{Fore.CYAN}{' '*20}{Style.BRIGHT}📚 COMMAND REFERENCE{Style.RESET_ALL}")
    help_text.append(_header_line() + "\n")

    # Basic Commands
    help_text.append(_section_line())
    help_text.append(f"{Fore.YELLOW}{Style.BRIGHT}BASIC COMMANDS{Style.RESET_ALL}")
    help_text.append(_section_line() + "\n")

    help_text.append(f"  {Fore.GREEN}{Command.HELLO}{Style.RESET_ALL}")
    help_text.append("    Greet the bot\n")

    help_text.append(f"  {Fore.GREEN}{Command.HELP}{Style.RESET_ALL} or {Fore.GREEN}{Command.HELP_ALT}{Style.RESET_ALL}")
    help_text.append("    Show this help message")
    help_text.append(f"    {Fore.CYAN}Usage:{Style.RESET_ALL} {Command.HELP} {Fore.BLUE}[category]{Style.RESET_ALL} or {Fore.BLUE}{Command.HELP} short{Style.RESET_ALL}\n")

    help_text.append(f"  {Fore.GREEN}{Command.STATS}{Style.RESET_ALL}")
    help_text.append("    Show comprehensive application statistics \n")

    help_text.append(f"  {Fore.GREEN}{Command.EXIT_1}{Style.RESET_ALL} or {Fore.GREEN}{Command.EXIT_2}{Style.RESET_ALL}")
    help_text.append("    Exit the program\n")

    # Contact Commands
    help_text.append(_section_line())
    help_text.append(f"{Fore.YELLOW}{Style.BRIGHT}CONTACT COMMANDS{Style.RESET_ALL}")
    help_text.append(_section_line() + "\n")

    help_text.append(f"  {Fore.GREEN}{Command.ADD_CONTACT}{Style.RESET_ALL} {Fore.MAGENTA}<name>{Style.RESET_ALL} {Fore.MAGENTA}<phone>{Style.RESET_ALL}")
    help_text.append("    Add a new contact or update existing")
    help_text.append(f"    {Fore.YELLOW}Example:{Style.RESET_ALL} {Fore.GREEN}{Command.ADD_CONTACT}{Style.RESET_ALL} {Fore.MAGENTA}\"John Doe\"{Style.RESET_ALL} {Fore.MAGENTA}1234567890{Style.RESET_ALL}")
    help_text.append(f"    {Fore.CYAN}Note:{Style.RESET_ALL} Phone must be {Phone.PHONE_LEN} digits\n")

    help_text.append(f"  {Fore.GREEN}{Command.SHOW_CONTACT}{Style.RESET_ALL} {Fore.MAGENTA}<name>{Style.RESET_ALL}")
    help_text.append("    Show contact information")
    help_text.append(f"    {Fore.YELLOW}Example:{Style.RESET_ALL} {Fore.GREEN}{Command.SHOW_CONTACT}{Style.RESET_ALL} {Fore.MAGENTA}\"John Doe\"{Style.RESET_ALL}\n")

    help_text.append(f"  {Fore.GREEN}{Command.SHOW_ALL_CONTACTS}{Style.RESET_ALL}")
    help_text.append("    Show all contacts in a formatted table\n")

    help_text.append(f"  {Fore.GREEN}{Command.SEARCH_CONTACTS}{Style.RESET_ALL} {Fore.MAGENTA}<value>{Style.RESET_ALL}")
    help_text.append("    Search contacts by name, phone, email, or address")
    help_text.append(f"    {Fore.YELLOW}Example:{Style.RESET_ALL} {Fore.GREEN}{Command.SEARCH_CONTACTS}{Style.RESET_ALL} {Fore.MAGENTA}John{Style.RESET_ALL}\n")

    help_text.append(f"  {Fore.GREEN}{Command.UPDATE_CONTACT}{Style.RESET_ALL} {Fore.MAGENTA}<name>{Style.RESET_ALL} {Fore.MAGENTA}<old_phone>{Style.RESET_ALL} {Fore.MAGENTA}<new_phone>{Style.RESET_ALL}")
    help_text.append("    Update contact's phone number")
    help_text.append(f"    {Fore.YELLOW}Example:{Style.RESET_ALL} {Fore.GREEN}{Command.UPDATE_CONTACT}{Style.RESET_ALL} {Fore.MAGENTA}\"John Doe\"{Style.RESET_ALL} {Fore.MAGENTA}1234567890{Style.RESET_ALL} {Fore.MAGENTA}0987654321{Style.RESET_ALL}\n")

    help_text.append(f"  {Fore.GREEN}{Command.DELETE_CONTACT}{Style.RESET_ALL} {Fore.MAGENTA}<name>{Style.RESET_ALL}")
    help_text.append("    Delete a contact (requires confirmation)")
    help_text.append(f"    {Fore.YELLOW}Example:{Style.RESET_ALL} {Fore.GREEN}{Command.DELETE_CONTACT}{Style.RESET_ALL} {Fore.MAGENTA}\"John Doe\"{Style.RESET_ALL}\n")

    # Birthday Commands
    help_text.append(_section_line())
    help_text.append(f"{Fore.YELLOW}{Style.BRIGHT}BIRTHDAY COMMANDS{Style.RESET_ALL}")
    help_text.append(_section_line() + "\n")

    help_text.append(f"  {Fore.GREEN}{Command.ADD_BIRTHDAY}{Style.RESET_ALL} {Fore.MAGENTA}<name>{Style.RESET_ALL} {Fore.MAGENTA}<{Birthday.DATE_FORMAT_DISPLAY}>{Style.RESET_ALL}")
    help_text.append("    Add or update contact's birthday")
    help_text.append(f"    {Fore.YELLOW}Example:{Style.RESET_ALL} {Fore.GREEN}{Command.ADD_BIRTHDAY}{Style.RESET_ALL} {Fore.MAGENTA}\"John Doe\"{Style.RESET_ALL} {Fore.MAGENTA}01.01.1990{Style.RESET_ALL}\n")

    help_text.append(f"  {Fore.GREEN}{Command.SHOW_BIRTHDAY}{Style.RESET_ALL} {Fore.MAGENTA}<name>{Style.RESET_ALL}")
    help_text.append("    Show contact's birthday")
    help_text.append(f"    {Fore.YELLOW}Example:{Style.RESET_ALL} {Fore.GREEN}{Command.SHOW_BIRTHDAY}{Style.RESET_ALL} {Fore.MAGENTA}\"John Doe\"{Style.RESET_ALL}\n")

    help_text.append(f"  {Fore.GREEN}{Command.SHOW_UPCOMING_BIRTHDAYS}{Style.RESET_ALL} {Fore.BLUE}[days]{Style.RESET_ALL}")
    help_text.append("    Show contacts with upcoming birthdays")
    help_text.append(f"    {Fore.YELLOW}Example:{Style.RESET_ALL} {Fore.GREEN}{Command.SHOW_UPCOMING_BIRTHDAYS}{Style.RESET_ALL} {Fore.BLUE}7{Style.RESET_ALL}")
    help_text.append(f"    {Fore.CYAN}Note:{Style.RESET_ALL} Default is 7 days if not specified\n")

    # Email Commands
    help_text.append(_section_line())
    help_text.append(f"{Fore.YELLOW}{Style.BRIGHT}EMAIL COMMANDS{Style.RESET_ALL}")
    help_text.append(_section_line() + "\n")

    help_text.append(f"  {Fore.GREEN}{Command.ADD_EMAIL}{Style.RESET_ALL} {Fore.MAGENTA}<name>{Style.RESET_ALL} {Fore.MAGENTA}<email>{Style.RESET_ALL}")
    help_text.append("    Add or update contact's email")
    help_text.append(f"    {Fore.YELLOW}Example:{Style.RESET_ALL} {Fore.GREEN}{Command.ADD_EMAIL}{Style.RESET_ALL} {Fore.MAGENTA}\"John Doe\"{Style.RESET_ALL} {Fore.MAGENTA}john@example.com{Style.RESET_ALL}\n")

    help_text.append(f"  {Fore.GREEN}{Command.SHOW_EMAIL}{Style.RESET_ALL} {Fore.MAGENTA}<name>{Style.RESET_ALL}")
    help_text.append("    Show contact's email")
    help_text.append(f"    {Fore.YELLOW}Example:{Style.RESET_ALL} {Fore.GREEN}{Command.SHOW_EMAIL}{Style.RESET_ALL} {Fore.MAGENTA}\"John Doe\"{Style.RESET_ALL}\n")

    help_text.append(f"  {Fore.GREEN}{Command.DELETE_EMAIL}{Style.RESET_ALL} {Fore.MAGENTA}<name>{Style.RESET_ALL}")
    help_text.append("    Delete contact's email")
    help_text.append(f"    {Fore.YELLOW}Example:{Style.RESET_ALL} {Fore.GREEN}{Command.DELETE_EMAIL}{Style.RESET_ALL} {Fore.MAGENTA}\"John Doe\"{Style.RESET_ALL}\n")

    # Address Commands
    help_text.append(_section_line())
    help_text.append(f"{Fore.YELLOW}{Style.BRIGHT}ADDRESS COMMANDS{Style.RESET_ALL}")
    help_text.append(_section_line() + "\n")

    help_text.append(f"  {Fore.GREEN}{Command.ADD_ADDRESS}{Style.RESET_ALL} {Fore.MAGENTA}<name>{Style.RESET_ALL} {Fore.MAGENTA}<address>{Style.RESET_ALL}")
    help_text.append("    Add a contact's address")
    help_text.append(f"    {Fore.YELLOW}Example:{Style.RESET_ALL} {Fore.GREEN}{Command.ADD_ADDRESS}{Style.RESET_ALL} {Fore.MAGENTA}\"John Doe\"{Style.RESET_ALL} {Fore.MAGENTA}456 Oak Avenue{Style.RESET_ALL}")

    help_text.append(f"  {Fore.GREEN}{Command.CHANGE_ADDRESS}{Style.RESET_ALL} {Fore.MAGENTA}<name>{Style.RESET_ALL} {Fore.MAGENTA}<address>{Style.RESET_ALL}")
    help_text.append("    Change a contact's address")
    help_text.append(f"    {Fore.YELLOW}Example:{Style.RESET_ALL} {Fore.GREEN}{Command.CHANGE_ADDRESS}{Style.RESET_ALL} {Fore.MAGENTA}\"John Doe\"{Style.RESET_ALL} {Fore.MAGENTA}315 Linkoln Street{Style.RESET_ALL}")

    help_text.append(f"  {Fore.GREEN}{Command.DELETE_ADDRESS}{Style.RESET_ALL} {Fore.MAGENTA}<name>{Style.RESET_ALL}")
    help_text.append("    Remove a contact's address")
    help_text.append(f"    {Fore.YELLOW}Example:{Style.RESET_ALL} {Fore.GREEN}{Command.DELETE_ADDRESS}{Style.RESET_ALL} {Fore.MAGENTA}\"John Doe\"{Style.RESET_ALL}")

    # Note Commands
    help_text.append(_section_line())
    help_text.append(f"{Fore.YELLOW}{Style.BRIGHT}NOTE COMMANDS{Style.RESET_ALL}")
    help_text.append(_section_line() + "\n")

    help_text.append(f"  {Fore.GREEN}{Command.ADD_NOTE}{Style.RESET_ALL} {Fore.MAGENTA}<text>{Style.RESET_ALL} {Fore.BLUE}[tags]{Style.RESET_ALL}")
    help_text.append("    Add a new note with optional tags")
    help_text.append(f"    {Fore.YELLOW}Example:{Style.RESET_ALL} {Fore.GREEN}{Command.ADD_NOTE}{Style.RESET_ALL} {Fore.MAGENTA}\"Call John\"{Style.RESET_ALL} {Fore.BLUE}work important{Style.RESET_ALL}\n")

    help_text.append(f"  {Fore.GREEN}{Command.LIST_NOTES}{Style.RESET_ALL} {Fore.BLUE}[sort]{Style.RESET_ALL}")
    help_text.append("    List all notes with optional sorting")
    help_text.append(f"    {Fore.YELLOW}Example:{Style.RESET_ALL} {Fore.GREEN}{Command.LIST_NOTES}{Style.RESET_ALL} {Fore.BLUE}created{Style.RESET_ALL}")
    help_text.append(f"    {Fore.RED}{Style.BRIGHT}Sort options:{Style.RESET_ALL} {Fore.CYAN}created{Style.RESET_ALL}, {Fore.CYAN}updated{Style.RESET_ALL}, {Fore.CYAN}text{Style.RESET_ALL}, {Fore.CYAN}tags{Style.RESET_ALL}\n")

    help_text.append(f"  {Fore.GREEN}{Command.SEARCH_NOTES}{Style.RESET_ALL} {Fore.MAGENTA}<query>{Style.RESET_ALL}")
    help_text.append("    Search notes by text or tags")
    help_text.append(f"    {Fore.YELLOW}Example:{Style.RESET_ALL} {Fore.GREEN}{Command.SEARCH_NOTES}{Style.RESET_ALL} {Fore.MAGENTA}meeting{Style.RESET_ALL}\n")

    help_text.append(f"  {Fore.GREEN}{Command.SEARCH_TAGS}{Style.RESET_ALL} {Fore.MAGENTA}<tags>{Style.RESET_ALL}")
    help_text.append("    Search notes by specific tags")
    help_text.append(f"    {Fore.YELLOW}Example:{Style.RESET_ALL} {Fore.GREEN}{Command.SEARCH_TAGS}{Style.RESET_ALL} {Fore.MAGENTA}work important{Style.RESET_ALL}\n")

    help_text.append(f"  {Fore.GREEN}{Command.EDIT_NOTE}{Style.RESET_ALL} {Fore.MAGENTA}<id>{Style.RESET_ALL} {Fore.MAGENTA}<text>{Style.RESET_ALL} {Fore.BLUE}[tags]{Style.RESET_ALL}")
    help_text.append("     Edit a note by ID or number")
    help_text.append(f"    {Fore.YELLOW}Example:{Style.RESET_ALL} {Fore.GREEN}{Command.EDIT_NOTE}{Style.RESET_ALL} {Fore.MAGENTA}1{Style.RESET_ALL} {Fore.MAGENTA}\"Updated text\"{Style.RESET_ALL} {Fore.BLUE}new-tag{Style.RESET_ALL}\n")

    help_text.append(f"  {Fore.GREEN}{Command.DELETE_NOTE}{Style.RESET_ALL} {Fore.MAGENTA}<id>{Style.RESET_ALL}")
    help_text.append("     Delete a note by ID or number")
    help_text.append(f"    {Fore.YELLOW}Example:{Style.RESET_ALL} {Fore.GREEN}{Command.DELETE_NOTE}{Style.RESET_ALL} {Fore.MAGENTA}1{Style.RESET_ALL}\n")


    # Tips
    help_text.append(_section_line())
    help_text.append(f"{Fore.YELLOW}{Style.BRIGHT}💡 TIPS{Style.RESET_ALL}")
    help_text.append(_section_line() + "\n")

    help_text.append(f"  • Use {Fore.CYAN}{Style.BRIGHT}quotes{Style.RESET_ALL} for names with spaces: {Command.ADD_CONTACT} {Fore.CYAN}\"John Doe\"{Style.RESET_ALL} 1234567890")
    help_text.append(f"  • Phone numbers must be exactly {Fore.YELLOW}{Style.BRIGHT}{Phone.PHONE_LEN} digits{Style.RESET_ALL}")
    help_text.append(f"  • Birthday format: {Fore.BLUE}{Style.BRIGHT}{Birthday.DATE_FORMAT_DISPLAY}{Style.RESET_ALL}")
    help_text.append(f"  • Tags can be separated by {Fore.YELLOW}{Style.BRIGHT} commas or spaces {Style.RESET_ALL}")
    help_text.append(f"  • Use {Fore.CYAN}{Command.SHOW_ALL_CONTACTS}{Style.RESET_ALL} to see all contacts in a table")
    help_text.append(f"  • Use {Fore.CYAN}{Command.HELP}{Style.RESET_ALL} {Fore.MAGENTA}<category>{Style.RESET_ALL} for category-specific help")
    help_text.append(f"    Available categories: {Fore.BLUE}contacts{Style.RESET_ALL}, {Fore.BLUE}notes{Style.RESET_ALL}, {Fore.BLUE}birthdays{Style.RESET_ALL}, {Fore.BLUE}email{Style.RESET_ALL}, {Fore.BLUE}address{Style.RESET_ALL}")

    help_text.append(f"\n{_header_line()}\n")

    return "\n".join(help_text)


def format_help_short():
    """
    Format short help with just command names.
    
    Returns:
        str: Short help text
    """
    help_text = []
    help_text.append(_header_line())
    help_text.append(f"{Fore.CYAN}{Style.BRIGHT}Quick Reference{Style.RESET_ALL}")
    help_text.append(_header_line() + "\n")

    help_text.append(f"{Fore.YELLOW}{Style.BRIGHT}Contacts:{Style.RESET_ALL}")
    help_text.append(f"  {Command.ADD_CONTACT}, {Command.SHOW_CONTACT}, {Command.SHOW_ALL_CONTACTS}")
    help_text.append(f"  {Command.SEARCH_CONTACTS}, {Command.UPDATE_CONTACT}, {Command.DELETE_CONTACT}")

    help_text.append(f"\n{Fore.YELLOW}{Style.BRIGHT}Birthdays:{Style.RESET_ALL}")
    help_text.append(f"  {Command.ADD_BIRTHDAY}, {Command.SHOW_BIRTHDAY}, {Command.SHOW_UPCOMING_BIRTHDAYS}")

    help_text.append(f"\n{Fore.YELLOW}{Style.BRIGHT}Email:{Style.RESET_ALL}")
    help_text.append(f"  {Command.ADD_EMAIL}, {Command.SHOW_EMAIL}, {Command.DELETE_EMAIL}")

    help_text.append(f"\n{Fore.YELLOW}{Style.BRIGHT}Notes:{Style.RESET_ALL}")
    help_text.append(f"  {Command.ADD_NOTE}, {Command.LIST_NOTES}, {Command.SEARCH_NOTES}")
    help_text.append(f"  {Command.SEARCH_TAGS}, {Command.EDIT_NOTE}, {Command.DELETE_NOTE}")

    help_text.append(f"\n{Fore.YELLOW}{Style.BRIGHT}Address:{Style.RESET_ALL}")
    help_text.append(f"  {Command.ADD_ADDRESS}, {Command.CHANGE_ADDRESS}, {Command.DELETE_ADDRESS}")

    help_text.append(f"\n{Fore.YELLOW}{Style.BRIGHT}System:{Style.RESET_ALL}")
    help_text.append(f"  {Command.HELLO}, {Command.HELP}, {Command.STATS}, {Command.EXIT_1}, {Command.EXIT_2}")

    help_text.append(f"\n{_header_line()}")
    help_text.append(f"{Fore.CYAN}Type '{Command.HELP}' for detailed information{Style.RESET_ALL}")
    help_text.append(f"{Fore.CYAN}Type '{Command.HELP} <category>' for category help{Style.RESET_ALL}")
    help_text.append(f"{_header_line()}\n")

    return "\n".join(help_text)


def format_help_category(category):
    """
    Format help for a specific category.
    
    Args:
        category: Category name (contacts, notes, birthdays, email)
        
    Returns:
        str: Category-specific help
    """
    category = category.lower()

    if category == "contacts":
        return format_contacts_help()
    elif category == "notes":
        return format_notes_help()
    elif category == "birthdays":
        return format_birthdays_help()
    elif category == "email":
        return format_email_help()
    elif category == "address":
        return format_address_help()
    else:
        return (
            f"{Fore.RED}Unknown category: '{category}'{Style.RESET_ALL}\n"
            f"{Fore.CYAN}Available categories:{Style.RESET_ALL} contacts, notes, birthdays, email, address"
        )


def format_contacts_help():
    """Format contacts-specific help."""
    help_text = []
    help_text.append(_header_line())
    help_text.append(f"{Fore.CYAN}{Style.BRIGHT}CONTACT COMMANDS{Style.RESET_ALL}")
    help_text.append(_header_line() + "\n")

    help_text.append(f"  {Fore.GREEN}{Command.ADD_CONTACT}{Style.RESET_ALL} {Fore.MAGENTA}<name>{Style.RESET_ALL} {Fore.MAGENTA}<phone>{Style.RESET_ALL}")
    help_text.append("    Add a new contact or update existing contact with phone number")
    help_text.append(f"    {Fore.YELLOW}Example:{Style.RESET_ALL} {Fore.GREEN}{Command.ADD_CONTACT}{Style.RESET_ALL} {Fore.MAGENTA}\"John Doe\"{Style.RESET_ALL} {Fore.MAGENTA}1234567890{Style.RESET_ALL}")
    help_text.append(f"    {Fore.CYAN}Note:{Style.RESET_ALL} Phone must be exactly {Phone.PHONE_LEN} digits")
    help_text.append(f"    {Fore.CYAN}Note:{Style.RESET_ALL} Use quotes for names with spaces\n")

    help_text.append(f"  {Fore.GREEN}{Command.SHOW_CONTACT}{Style.RESET_ALL} {Fore.MAGENTA}<name>{Style.RESET_ALL}")
    help_text.append("    Show detailed information about a specific contact")
    help_text.append(f"    {Fore.YELLOW}Example:{Style.RESET_ALL} {Fore.GREEN}{Command.SHOW_CONTACT}{Style.RESET_ALL} {Fore.MAGENTA}\"John Doe\"{Style.RESET_ALL}\n")

    help_text.append(f"  {Fore.GREEN}{Command.SHOW_ALL_CONTACTS}{Style.RESET_ALL}")
    help_text.append("    Display all contacts in a formatted table")
    help_text.append("    Shows: Name, Phones, Email, Birthday\n")

    help_text.append(f"  {Fore.GREEN}{Command.SEARCH_CONTACTS}{Style.RESET_ALL} {Fore.MAGENTA}<value>{Style.RESET_ALL}")
    help_text.append("    Search contacts by name, phone, email, or address")
    help_text.append(f"    {Fore.YELLOW}Example:{Style.RESET_ALL} {Fore.GREEN}{Command.SEARCH_CONTACTS}{Style.RESET_ALL} {Fore.MAGENTA}John{Style.RESET_ALL}\n")

    help_text.append(f"  {Fore.GREEN}{Command.UPDATE_CONTACT}{Style.RESET_ALL} {Fore.MAGENTA}<name>{Style.RESET_ALL} {Fore.MAGENTA}<old_phone>{Style.RESET_ALL} {Fore.MAGENTA}<new_phone>{Style.RESET_ALL}")
    help_text.append("    Update an existing phone number for a contact")
    help_text.append(f"    {Fore.YELLOW}Example:{Style.RESET_ALL} {Fore.GREEN}{Command.UPDATE_CONTACT}{Style.RESET_ALL} {Fore.MAGENTA}\"John Doe\"{Style.RESET_ALL} {Fore.MAGENTA}1234567890{Style.RESET_ALL} {Fore.MAGENTA}0987654321{Style.RESET_ALL}")
    help_text.append(f"    {Fore.CYAN}Note:{Style.RESET_ALL} Both phones must be exactly {Phone.PHONE_LEN} digits\n")

    help_text.append(f"  {Fore.GREEN}{Command.DELETE_CONTACT}{Style.RESET_ALL} {Fore.MAGENTA}<name>{Style.RESET_ALL}")
    help_text.append("    Delete a contact from the address book")
    help_text.append(f"    {Fore.YELLOW}Example:{Style.RESET_ALL} {Fore.GREEN}{Command.DELETE_CONTACT}{Style.RESET_ALL} {Fore.MAGENTA}\"John Doe\"{Style.RESET_ALL}")
    help_text.append(f"    {Fore.CYAN}Note:{Style.RESET_ALL} Requires confirmation before deletion\n")

    help_text.append(f"{_header_line()}\n")

    return "\n".join(help_text)


def format_notes_help():
    """Format notes-specific help."""
    help_text = []
    help_text.append(_header_line())
    help_text.append(f"{Fore.CYAN}{Style.BRIGHT}NOTE COMMANDS{Style.RESET_ALL}")
    help_text.append(f"{_header_line()}\n")

    help_text.append(f"  {Fore.GREEN}{Command.ADD_NOTE}{Style.RESET_ALL} {Fore.MAGENTA}<text>{Style.RESET_ALL} {Fore.BLUE}[tags]{Style.RESET_ALL}")
    help_text.append("    Add a new note with optional tags")
    help_text.append(f"    {Fore.YELLOW}Example:{Style.RESET_ALL} {Fore.GREEN}{Command.ADD_NOTE}{Style.RESET_ALL} {Fore.MAGENTA}\"Call John tomorrow\"{Style.RESET_ALL} {Fore.BLUE}work important{Style.RESET_ALL}")
    help_text.append(f"    {Fore.YELLOW}Example:{Style.RESET_ALL} {Fore.GREEN}{Command.ADD_NOTE}{Style.RESET_ALL} {Fore.MAGENTA}\"Meeting notes\"{Style.RESET_ALL} {Fore.BLUE}work,meeting{Style.RESET_ALL}")
    help_text.append(f"    {Fore.CYAN}Note:{Style.RESET_ALL} Tags can be separated by commas or spaces\n")

    help_text.append(f"  {Fore.GREEN}{Command.LIST_NOTES}{Style.RESET_ALL} {Fore.BLUE}[sort]{Style.RESET_ALL}")
    help_text.append("    List all notes with optional sorting")
    help_text.append(f"    {Fore.YELLOW}Example:{Style.RESET_ALL} {Fore.GREEN}{Command.LIST_NOTES}{Style.RESET_ALL}")
    help_text.append(f"    {Fore.YELLOW}Example:{Style.RESET_ALL} {Fore.GREEN}{Command.LIST_NOTES}{Style.RESET_ALL} {Fore.BLUE}created{Style.RESET_ALL}")
    help_text.append(f"    {Fore.CYAN}Sort options:{Style.RESET_ALL}")
    help_text.append("      - created: Sort by creation date (newest first)")
    help_text.append("      - updated: Sort by last update date (newest first)")
    help_text.append("      - tags: Sort alphabetically by first tag")
    help_text.append("      - text: Sort alphabetically by text")

    help_text.append(f"  {Fore.GREEN}{Command.SEARCH_NOTES}{Style.RESET_ALL} {Fore.MAGENTA}<query>{Style.RESET_ALL}")
    help_text.append("    Search notes by text content or tags")
    help_text.append(f"    {Fore.YELLOW}Example:{Style.RESET_ALL} {Fore.GREEN}{Command.SEARCH_NOTES}{Style.RESET_ALL} {Fore.MAGENTA}meeting{Style.RESET_ALL}")
    help_text.append(f"    {Fore.YELLOW}Example:{Style.RESET_ALL} {Fore.GREEN}{Command.SEARCH_NOTES}{Style.RESET_ALL} {Fore.MAGENTA}john{Style.RESET_ALL}")
    help_text.append(f"    {Fore.CYAN}Note:{Style.RESET_ALL} Searches in both note text and tags\n")

    help_text.append(f"  {Fore.GREEN}{Command.SEARCH_TAGS}{Style.RESET_ALL} {Fore.MAGENTA}<tags>{Style.RESET_ALL}")
    help_text.append("    Search notes by specific tags only")
    help_text.append(f"    {Fore.YELLOW}Example:{Style.RESET_ALL} {Fore.GREEN}{Command.SEARCH_TAGS}{Style.RESET_ALL} {Fore.MAGENTA}work important{Style.RESET_ALL}")
    help_text.append(f"    {Fore.CYAN}Note:{Style.RESET_ALL} Tags can be separated by commas or spaces\n")

    help_text.append(f"  {Fore.GREEN}{Command.EDIT_NOTE}{Style.RESET_ALL} {Fore.MAGENTA}<id>{Style.RESET_ALL} {Fore.MAGENTA}<text>{Style.RESET_ALL} {Fore.BLUE}[tags]{Style.RESET_ALL}")
    help_text.append("    Edit a note by its ID or number (from list)")
    help_text.append(f"    {Fore.YELLOW}Example:{Style.RESET_ALL} {Fore.GREEN}{Command.EDIT_NOTE}{Style.RESET_ALL} {Fore.MAGENTA}1{Style.RESET_ALL} {Fore.MAGENTA}\"Updated text\"{Style.RESET_ALL} {Fore.BLUE}new-tag{Style.RESET_ALL}")
    help_text.append(f"    {Fore.YELLOW}Example:{Style.RESET_ALL} {Fore.GREEN}{Command.EDIT_NOTE}{Style.RESET_ALL} {Fore.MAGENTA}abc123{Style.RESET_ALL} {Fore.MAGENTA}\"New text\"{Style.RESET_ALL} {Fore.BLUE}tag1 tag2{Style.RESET_ALL}")
    help_text.append(f"    {Fore.CYAN}Note:{Style.RESET_ALL} Use note number from {Command.LIST_NOTES} or full UUID\n")

    help_text.append(f"  {Fore.GREEN}{Command.DELETE_NOTE}{Style.RESET_ALL} {Fore.MAGENTA}<id>{Style.RESET_ALL}")
    help_text.append("    Delete a note by its ID or number")
    help_text.append(f"    {Fore.YELLOW}Example:{Style.RESET_ALL} {Fore.GREEN}{Command.DELETE_NOTE}{Style.RESET_ALL} {Fore.MAGENTA}1{Style.RESET_ALL}")
    help_text.append(f"    {Fore.YELLOW}Example:{Style.RESET_ALL} {Fore.GREEN}{Command.DELETE_NOTE}{Style.RESET_ALL} {Fore.MAGENTA}abc123{Style.RESET_ALL}")
    help_text.append(f"    {Fore.CYAN}Note:{Style.RESET_ALL} Use note number from {Command.LIST_NOTES} or full UUID\n")

    help_text.append(f"{_header_line()}\n")

    return "\n".join(help_text)


def format_birthdays_help():
    """Format birthdays-specific help."""
    help_text = []
    help_text.append(_header_line())
    help_text.append(f"{Fore.CYAN}{Style.BRIGHT}BIRTHDAY COMMANDS{Style.RESET_ALL}")
    help_text.append(f"{_header_line()}\n")

    help_text.append(f"  {Fore.GREEN}{Command.ADD_BIRTHDAY}{Style.RESET_ALL} {Fore.MAGENTA}<name>{Style.RESET_ALL} {Fore.MAGENTA}<{Birthday.DATE_FORMAT_DISPLAY}>{Style.RESET_ALL}")
    help_text.append("    Add or update contact's birthday")
    help_text.append(f"    {Fore.YELLOW}Example:{Style.RESET_ALL} {Fore.GREEN}{Command.ADD_BIRTHDAY}{Style.RESET_ALL} {Fore.MAGENTA}\"Jane Smith\"{Style.RESET_ALL} {Fore.MAGENTA}15.03.1985{Style.RESET_ALL}")
    help_text.append(f"    {Fore.CYAN}Format:{Style.RESET_ALL} {Birthday.DATE_FORMAT_DISPLAY} (DD.MM.YYYY)")
    help_text.append(f"    {Fore.CYAN}Note:{Style.RESET_ALL} Use quotes for names with spaces\n")

    help_text.append(f"  {Fore.GREEN}{Command.SHOW_BIRTHDAY}{Style.RESET_ALL} {Fore.MAGENTA}<name>{Style.RESET_ALL}")
    help_text.append("    Show contact's birthday information")
    help_text.append(f"    {Fore.YELLOW}Example:{Style.RESET_ALL} {Fore.GREEN}{Command.SHOW_BIRTHDAY}{Style.RESET_ALL} {Fore.MAGENTA}\"John Doe\"{Style.RESET_ALL}")
    help_text.append(f"    {Fore.CYAN}Note:{Style.RESET_ALL} Shows birthday with age and days until next birthday\n")

    help_text.append(f"  {Fore.GREEN}{Command.SHOW_UPCOMING_BIRTHDAYS}{Style.RESET_ALL} {Fore.BLUE}[days]{Style.RESET_ALL}")
    help_text.append("    Show contacts with upcoming birthdays within specified days")
    help_text.append(f"    {Fore.YELLOW}Example:{Style.RESET_ALL} {Fore.GREEN}{Command.SHOW_UPCOMING_BIRTHDAYS}{Style.RESET_ALL}")
    help_text.append(f"    {Fore.YELLOW}Example:{Style.RESET_ALL} {Fore.GREEN}{Command.SHOW_UPCOMING_BIRTHDAYS}{Style.RESET_ALL} {Fore.BLUE}7{Style.RESET_ALL}")
    help_text.append(f"    {Fore.YELLOW}Example:{Style.RESET_ALL} {Fore.GREEN}{Command.SHOW_UPCOMING_BIRTHDAYS}{Style.RESET_ALL} {Fore.BLUE}14{Style.RESET_ALL}")
    help_text.append(f"    {Fore.CYAN}Note:{Style.RESET_ALL} Default is 7 days if not specified")
    help_text.append(f"    {Fore.CYAN}Note:{Style.RESET_ALL} Shows birthdays within the next N days\n")

    help_text.append(f"{_header_line()}\n")

    return "\n".join(help_text)


def format_email_help():
    """Format email-specific help."""
    help_text = []
    help_text.append(_header_line())
    help_text.append(f"{Fore.CYAN}{Style.BRIGHT}EMAIL COMMANDS{Style.RESET_ALL}")
    help_text.append(f"{_header_line()}\n")

    help_text.append(f"  {Fore.GREEN}{Command.ADD_EMAIL}{Style.RESET_ALL} {Fore.MAGENTA}<name>{Style.RESET_ALL} {Fore.MAGENTA}<email>{Style.RESET_ALL}")
    help_text.append("    Add or update contact's email address")
    help_text.append(f"    {Fore.YELLOW}Example:{Style.RESET_ALL} {Fore.GREEN}{Command.ADD_EMAIL}{Style.RESET_ALL} {Fore.MAGENTA}\"Jane Smith\"{Style.RESET_ALL} {Fore.MAGENTA}jane.smith@company.com{Style.RESET_ALL}")
    help_text.append(f"    {Fore.CYAN}Note:{Style.RESET_ALL} Email must be in valid format (user@domain.com)")
    help_text.append(f"    {Fore.CYAN}Note:{Style.RESET_ALL} Each contact can have only one email")
    help_text.append(f"    {Fore.CYAN}Note:{Style.RESET_ALL} Updating email replaces the existing one\n")

    help_text.append(f"  {Fore.GREEN}{Command.SHOW_EMAIL}{Style.RESET_ALL} {Fore.MAGENTA}<name>{Style.RESET_ALL}")
    help_text.append("    Show contact's email address")
    help_text.append(f"    {Fore.YELLOW}Example:{Style.RESET_ALL} {Fore.GREEN}{Command.SHOW_EMAIL}{Style.RESET_ALL} {Fore.MAGENTA}\"John Doe\"{Style.RESET_ALL}")
    help_text.append(f"    {Fore.CYAN}Note:{Style.RESET_ALL} Shows 'No email' if contact has no email set\n")

    help_text.append(f"  {Fore.GREEN}{Command.DELETE_EMAIL}{Style.RESET_ALL} {Fore.MAGENTA}<name>{Style.RESET_ALL}")
    help_text.append("    Delete contact's email address")
    help_text.append(f"    {Fore.YELLOW}Example:{Style.RESET_ALL} {Fore.GREEN}{Command.DELETE_EMAIL}{Style.RESET_ALL} {Fore.MAGENTA}\"John Doe\"{Style.RESET_ALL}")
    help_text.append(f"    {Fore.CYAN}Note:{Style.RESET_ALL} Removes email from contact (contact remains)\n")

    help_text.append(f"{_header_line()}\n")

    return "\n".join(help_text)

def format_address_help():
    """Format address-specific help."""
    help_text = []
    help_text.append(_header_line())
    help_text.append(f"{Fore.CYAN}{Style.BRIGHT}ADDRESS COMMANDS{Style.RESET_ALL}")
    help_text.append(f"{_header_line()}\n")

    help_text.append(f"  {Fore.GREEN}{Command.ADD_ADDRESS}{Style.RESET_ALL} {Fore.MAGENTA}<name>{Style.RESET_ALL} {Fore.MAGENTA}<address>{Style.RESET_ALL}")
    help_text.append("    Add or update contact's address")
    help_text.append(f"    {Fore.YELLOW}Example:{Style.RESET_ALL} {Fore.GREEN}{Command.ADD_ADDRESS}{Style.RESET_ALL} {Fore.MAGENTA}\"John Doe\"{Style.RESET_ALL} {Fore.MAGENTA}456 Oak Avenue{Style.RESET_ALL}")
    help_text.append(f"    {Fore.CYAN}Note:{Style.RESET_ALL} Address can contain multiple words")
    help_text.append(f"    {Fore.CYAN}Note:{Style.RESET_ALL} Each contact can have only one address")
    help_text.append(f"    {Fore.CYAN}Note:{Style.RESET_ALL} Updating address replaces the existing one\n")

    help_text.append(f"  {Fore.GREEN}{Command.CHANGE_ADDRESS}{Style.RESET_ALL} {Fore.MAGENTA}<name>{Style.RESET_ALL} {Fore.MAGENTA}<new_address>{Style.RESET_ALL}")
    help_text.append("    Change contact's address")
    help_text.append(f"    {Fore.YELLOW}Example:{Style.RESET_ALL} {Fore.GREEN}{Command.CHANGE_ADDRESS}{Style.RESET_ALL} {Fore.MAGENTA}\"John Doe\"{Style.RESET_ALL} {Fore.MAGENTA}789 Pine Road Suite 100{Style.RESET_ALL}")
    help_text.append(f"    {Fore.CYAN}Note:{Style.RESET_ALL} Replaces existing address with new one\n")

    help_text.append(f"  {Fore.GREEN}{Command.DELETE_ADDRESS}{Style.RESET_ALL} {Fore.MAGENTA}<name>{Style.RESET_ALL}")
    help_text.append("    Delete contact's address")
    help_text.append(f"    {Fore.YELLOW}Example:{Style.RESET_ALL} {Fore.GREEN}{Command.DELETE_ADDRESS}{Style.RESET_ALL} {Fore.MAGENTA}\"John Doe\"{Style.RESET_ALL}")
    help_text.append(f"    {Fore.CYAN}Note:{Style.RESET_ALL} Removes address from contact (contact remains)\n")

    help_text.append(f"{_header_line()}\n")

    return "\n".join(help_text)