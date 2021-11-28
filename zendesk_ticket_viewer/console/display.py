import rich
from api.ticket_service import APIErrorException

def display_message(message: str) -> None:
    rich.print(message)

def display_warning(message: str) -> None:
    rich.print(f"[yellow]{message}[/]")

def display_error(message: str) -> None:
    rich.print(f"[red]{message}[/]")

def display_api_error(err: APIErrorException) -> None:
    display_error(err.message)
    resp = err.resp["error"] if "error" in err.resp else ""
    display_message(f"Status Code: {err.status_code}, {resp}")

def display_single_ticket(ticket: dict) -> None:
    rich.print_json(data=ticket)
