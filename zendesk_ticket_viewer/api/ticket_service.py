import requests
from typing import Union
from config import URL, USER_EMAIL, USER_PASSWORD

class APIErrorException(Exception):
    """Raised when the request to api fails"""
    def __init__(self, status_code: int, resp: dict, message: str):
        self.status_code = status_code
        self.resp = resp
        self.message = message
        super().__init__(self.message)

def call_get_api(endpoint: str) -> Union[dict, list[dict]]:
    """GET request an api and returns its json format respond"""
    request_url = URL + endpoint
    resp = requests.get(request_url, auth=(USER_EMAIL, USER_PASSWORD))
    if resp.status_code != 200:
        raise APIErrorException(resp.status_code, resp.json(), f"Failed api request: {request_url}")

    return resp.json()
