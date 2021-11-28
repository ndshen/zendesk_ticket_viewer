from typing import Callable
from api.ticket_service import call_get_api
from console.display import display_message, display_single_ticket, display_ticket_list
from config import URL, PAGINATION_SIZE


class CommandSyntaxException(Exception):
    """Raised when the command is not called correctly"""
    pass

def quit(**kwargs: dict) -> None:
    if kwargs["payload"] != "quit":
        raise CommandSyntaxException("Usage: quit")
    
    display_message("See you next time!")
    exit(0)

def show_ticket(**kwargs: dict) -> None:
    payload_objs = kwargs["payload"].split(" ")
    if len(payload_objs) != 2 or payload_objs[1].isnumeric() is not True:
        raise CommandSyntaxException("Usage: show <ticket_id>")
    
    ticket_id = int(payload_objs[1])
    endpoint = f"/api/v2/tickets/{ticket_id}.json"
    resp = call_get_api(endpoint)
    display_single_ticket(resp["ticket"])

def generate_list_ticket_action(endpoint=None) -> Callable:
    if endpoint is None:
        endpoint = f"/api/v2/tickets?page[size]={PAGINATION_SIZE}"

    def list_tickets(**kwargs: dict) -> None:
        resp = call_get_api(endpoint)
        tickets = resp["tickets"]
        links = resp["links"]

        if len(tickets) == 0:
            payload = kwargs["payload"]
            cmd = payload.split(" ")[0]
            if cmd == "p":
                display_message("currently the first page")
            elif cmd == "n":
                display_message("currently the last page")
            elif cmd == "list":
                display_message("the list is empty")
            
            return
        
        repl = kwargs["repl"]
        prev_endpoint = links["prev"].replace(URL, "")
        next_endpoint = links["next"].replace(URL, "")

        repl.add_extended_command("p", generate_list_ticket_action(prev_endpoint))
        repl.add_extended_command("n", generate_list_ticket_action(next_endpoint))

        display_ticket_list(tickets)
    
    return list_tickets
