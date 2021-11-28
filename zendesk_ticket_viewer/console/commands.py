from api.ticket_service import get_ticket
from console.display import display_message, display_single_ticket


class CommandSyntaxException(Exception):
    """Raised when the command is not called correctly"""
    pass

def quit(payload: str) -> None:
    if payload != "quit":
        raise CommandSyntaxException("Usage: quit")
    
    display_message("See you next time!")
    exit(0)

def show_ticket(payload: str) -> None:
    payload_objs = payload.split(" ")
    if len(payload_objs) != 2 or payload_objs[1].isnumeric() is not True:
        raise CommandSyntaxException("Usage: show <ticket_id>")
    
    ticket_id = int(payload_objs[1])
    ticket = get_ticket(ticket_id)
    display_single_ticket(ticket)
