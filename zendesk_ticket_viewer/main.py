from requests.api import get
from api.ticket_service import get_ticket
from console.repl import Repl
from console.commands import show_ticket, quit


def main() -> None:
    repl = Repl()
    repl.add_command("quit", quit, "Exit the program")
    repl.add_command("show", show_ticket, "Get the information of the ticket. Usage: show <ticket_id>")
    repl.run()

if __name__ == "__main__":
    main()