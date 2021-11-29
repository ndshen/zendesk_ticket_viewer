import unittest

from zendesk_ticket_viewer.api.ticket_service import APIErrorException, call_get_api

class TestTicketService(unittest.TestCase):
    def test_call_get_api(self):
        endpoint = "/api/v2/tickets"
        try:
            call_get_api(endpoint)
        except APIErrorException:
            self.fail(f"call_get_api() fails to request {endpoint}")
        
        invlaid_endpoint = "/api/v2/ticke"
        try:
            call_get_api(invlaid_endpoint)
        except APIErrorException as err:
            self.assertTrue(hasattr(err, "status_code"))
            self.assertTrue(hasattr(err, "resp"))
            self.assertTrue(hasattr(err, "message"))
        else:
            self.fail("should raise APIErrorException for invalid endpoint")
