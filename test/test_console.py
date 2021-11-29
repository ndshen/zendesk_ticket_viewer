import unittest
from io import StringIO
from unittest.mock import patch

from zendesk_ticket_viewer.api.ticket_service import APIErrorException
from zendesk_ticket_viewer.config import PROMPT
from zendesk_ticket_viewer.console.commands import quit
from zendesk_ticket_viewer.console.repl import Repl


class TestDisplayer:
    def display_prompt(self, prompt: str) -> None:
        print(prompt, end="")

    def display_message(self, message: str) -> None:
        print(message)

    def display_warning(self, message: str) -> None:
        print(message)

    def display_error(self, message: str) -> None:
        print(message)

    def display_api_error(self, err: APIErrorException) -> None:
        self.display_error(err.message)
        resp = err.resp["error"] if "error" in err.resp else ""
        self.display_message(f"Status Code: {err.status_code}, {resp}")

    def display_single_ticket(self, ticket: dict) -> None:
        print(ticket)

    def display_ticket_list(self, tickets: list[dict]) -> None:
        print(tickets)


class TestTicketService(unittest.TestCase):
    def setUp(self) -> None:
        self.repl = Repl(
            repl_displayer=TestDisplayer(), is_show_prompt=False, show_welcome=False
        )
        return super().setUp()

    def test_repl_help(self):
        self.repl.add_command("t1", self.dummy_action, "t1 help string")

        with patch("builtins.input", return_value="help"), patch(
            "sys.stdout", new=StringIO()
        ) as o:
            self.repl.run(single_command=True)
            self.assertEqual(o.getvalue(), "  t1: t1 help string\n")

    def test_show_prompt(self):
        with patch("sys.stdout", new=StringIO()) as o:
            self.repl._show_prompt()
            self.assertEqual(o.getvalue(), "")

        # should not show prompt
        with_prompt_repl = Repl(
            repl_displayer=TestDisplayer(), is_show_prompt=True, show_welcome=False
        )
        with patch("sys.stdout", new=StringIO()) as o:
            with_prompt_repl._show_prompt()
            self.assertEqual(o.getvalue(), PROMPT)

    def test_execute_action(self):
        def hello_world(**kwargs) -> None:
            print("hello world")

        self.repl.add_command("hello", hello_world, "print hello world")
        with patch("builtins.input", return_value="hello"), patch(
            "sys.stdout", new=StringIO()
        ) as o:
            self.repl.run(single_command=True)
            self.assertEqual(o.getvalue(), "hello world\n")

    def test_quit_action(self):
        self.repl.add_command("quit", quit, "Exit the program")
        with patch("builtins.input", return_value="quit"), patch(
            "sys.stdout", new=StringIO()
        ) as o:
            with self.assertRaises(SystemExit):
                self.repl.run(single_command=True)

    @staticmethod
    def dummy_action(kwargs):
        return
