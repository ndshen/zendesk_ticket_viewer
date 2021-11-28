import requests

class APIErrorException(Exception):
    """Raised when the request to api fails"""
    def __init__(self, status_code: int, resp: dict, message: str):
        self.status_code = status_code
        self.resp = resp
        self.message = message
        super().__init__(self.message)

URL = "https://zccndshen.zendesk.com"
USER_EMAIL = "ping-yao_shen@brown.edu"
USER_PASSWORD = "ndshenzendesk"

def get_ticket(ticket_id: int) -> dict:
    """Returns a ticket json object"""
    
    endpoint = f"/api/v2/tickets/{ticket_id}.json"
    request_url = URL + endpoint

    resp = requests.get(request_url, auth=(USER_EMAIL, USER_PASSWORD))
    if resp.status_code != 200:
        raise APIErrorException(resp.status_code, resp.json(), f"Failed api request: {request_url}")

    return resp.json()

