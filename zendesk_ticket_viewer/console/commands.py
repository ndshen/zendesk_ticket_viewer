from typing import Callable
from api.ticket_service import call_get_api
from config import URL, PAGINATION_SIZE


class CommandSyntaxException(Exception):
    """Raised when the command is not called correctly"""
    pass

def quit(**kwargs: dict) -> None:
    if kwargs["payload"] != "quit":
        raise CommandSyntaxException("Usage: quit")
    
    repl = kwargs["repl"]
    repl.repl_displayer.display_message("See you next time!")
    exit(0)

def show_ticket(**kwargs: dict) -> None:
    payload_objs = kwargs["payload"].split(" ")
    if len(payload_objs) != 2 or payload_objs[1].isnumeric() is not True:
        raise CommandSyntaxException("Usage: show <ticket_id>")
    
    ticket_id = int(payload_objs[1])
    endpoint = f"/api/v2/tickets/{ticket_id}.json"
    resp = call_get_api(endpoint)

    repl = kwargs["repl"]
    repl.repl_displayer.display_single_ticket(resp["ticket"])

def generate_list_ticket_action(endpoint=None) -> Callable:
    if endpoint is None:
        endpoint = f"/api/v2/tickets?page[size]={PAGINATION_SIZE}"

    def list_tickets(**kwargs: dict) -> None:
        repl = kwargs["repl"]

        resp = call_get_api(endpoint)
        tickets = resp["tickets"]
        links = resp["links"]

        if len(tickets) == 0:
            payload = kwargs["payload"]
            cmd = payload.split(" ")[0]
            if cmd == "p":
                repl.repl_displayer.display_message("currently the first page")
            elif cmd == "n":
                repl.repl_displayer.display_message("currently the last page")
            elif cmd == "list":
                repl.repl_displayer.display_message("the list is empty")
            
            return
        
        prev_endpoint = links["prev"].replace(URL, "")
        next_endpoint = links["next"].replace(URL, "")

        repl.add_extended_command("p", generate_list_ticket_action(prev_endpoint))
        repl.add_extended_command("n", generate_list_ticket_action(next_endpoint))

        repl.repl_displayer.display_ticket_list(tickets)
    
    return list_tickets
