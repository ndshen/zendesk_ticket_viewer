from rich.console import Console
from rich.table import Table
from rich.style import Style
from rich.color import Color
from api.ticket_service import APIErrorException

console = Console()

def display_prompt(prompt: str) -> None:
    console.print(prompt, style=Style(bgcolor=Color.from_rgb(0, 54, 61), color="white", bold=True) ,end="")

def display_message(message: str) -> None:
    console.print(message)

def display_warning(message: str) -> None:
    console.print(message, style=Style(color="yellow"))

def display_error(message: str) -> None:
    console.print(message, style=Style(color="red"))

def display_api_error(err: APIErrorException) -> None:
    display_error(err.message)
    resp = err.resp["error"] if "error" in err.resp else ""
    display_message(f"Status Code: {err.status_code}, {resp}")

def display_single_ticket(ticket: dict) -> None:
    table = Table.grid(padding=(1,3), pad_edge=True)
    table.add_column("Name", no_wrap=True, justify="left", style=Style(bold=True, color=Color.from_rgb(32,178,170)))
    table.add_column("Content")

    table.add_row("Subject", ticket.get("subject", ""))
    table.add_row("Created At", ticket.get("created_at", ""))
    table.add_row("Status", ticket.get("status", ""))
    table.add_row("Description", ticket.get("description", ""))

    console.print(table)

def display_ticket_list(tickets: list[dict]) -> None:
    table = Table(show_header=True, header_style=Style(bold=True, color=Color.from_rgb(32,178,170)), caption="'p' to previous page, 'n' to next page")
    table.add_column("Id", style="dim")
    table.add_column("Status")
    table.add_column("Subject")
    table.add_column("Created at")
    for ticket in tickets:
        ticket_id = str(ticket.get("id", ""))
        status = ticket.get("status", "")
        created_at = ticket.get("created_at", "")
        subject = ticket.get("subject", "")

        table.add_row(ticket_id, status, subject, created_at)
    
    console.print(table)