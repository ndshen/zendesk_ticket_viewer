from console.repl import Repl
from console.commands import generate_list_ticket_action, show_ticket, quit
from console.display import RichDisplayer

from config import USE_PROMPT


def main() -> None:
    repl = Repl(repl_displayer=RichDisplayer(), is_show_prompt=USE_PROMPT)
    repl.add_command("quit", quit, "Exit the program")
    repl.add_command("show", show_ticket, "Get the information of the ticket. Usage: show <ticket_id>")
    repl.add_command("list", generate_list_ticket_action(), "Get a list of tickets")
    repl.run()

if __name__ == "__main__":
    main()