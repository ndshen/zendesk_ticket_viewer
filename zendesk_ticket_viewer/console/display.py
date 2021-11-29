from api.ticket_service import APIErrorException
from rich.color import Color
from rich.console import Console
from rich.style import Style
from rich.table import Table

from config import PROMPT_BGCOLOR_RGB, PROMPT_COLOR_RGB


class RichDisplayer:
    def __init__(self):
        self.console = Console()

    def display_prompt(self, prompt: str) -> None:
        self.console.print(
            prompt,
            style=Style(
                bgcolor=Color.from_rgb(*PROMPT_BGCOLOR_RGB),
                color=Color.from_rgb(*PROMPT_COLOR_RGB),
                bold=True,
            ),
            end="",
        )

    def display_message(self, message: str) -> None:
        self.console.print(message)

    def display_warning(self, message: str) -> None:
        self.console.print(message, style=Style(color="yellow"))

    def display_error(self, message: str) -> None:
        self.console.print(message, style=Style(color="red"))

    def display_api_error(self, err: APIErrorException) -> None:
        self.display_error(err.message)
        resp = err.resp["error"] if "error" in err.resp else ""
        self.display_message(f"Status Code: {err.status_code}, {resp}")

    def display_single_ticket(self, ticket: dict) -> None:
        table = Table.grid(padding=(1, 3), pad_edge=True)
        table.add_column(
            "Name",
            no_wrap=True,
            justify="left",
            style=Style(bold=True, color=Color.from_rgb(32, 178, 170)),
        )
        table.add_column("Content")

        table.add_row("Subject", ticket.get("subject", ""))
        table.add_row("Created At", ticket.get("created_at", ""))
        table.add_row("Status", ticket.get("status", ""))
        table.add_row("Description", ticket.get("description", ""))

        self.console.print(table)

    def display_ticket_list(self, tickets: list[dict]) -> None:
        table = Table(
            show_header=True,
            header_style=Style(bold=True, color=Color.from_rgb(32, 178, 170)),
            caption="'p' to previous page, 'n' to next page",
        )
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

        self.console.print(table)
