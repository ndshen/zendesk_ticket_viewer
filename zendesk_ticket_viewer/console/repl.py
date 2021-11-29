from typing import Callable

from api.ticket_service import APIErrorException
from config import PROMPT
from console.commands import CommandSyntaxException


class Repl:
    prompt = PROMPT
    welcome_msg = "Welcome to zendesk ticket viewer.\nType 'help' to see all the commands or 'quit' to exit the program."

    def __init__(self, repl_displayer, is_show_prompt=True, show_welcome=True) -> None:
        self.repl_displayer = repl_displayer
        self.is_show_prompt = is_show_prompt
        self.show_welcome = show_welcome
        self.commands = dict()
        self.extended_commands = dict()

    def add_command(self, cmd: str, action: Callable, help_str: str) -> None:
        self.commands[cmd] = dict()
        self.commands[cmd]["action"] = action
        self.commands[cmd]["help"] = help_str

    def add_extended_command(self, cmd: str, action: Callable) -> None:
        self.extended_commands[cmd] = action

    def clear_extended_command(self) -> None:
        self.extended_commands = dict()

    def get_help(self) -> None:
        indent = "  "
        for key, val in self.commands.items():
            self.repl_displayer.display_message(f"{indent}{key}: {val['help']}")

    def _show_prompt(self) -> None:
        if self.is_show_prompt:
            self.repl_displayer.display_prompt(self.prompt)

    def run(self, single_command=False) -> None:
        if self.show_welcome:
            self.repl_displayer.display_message(self.welcome_msg)

        self._show_prompt()

        while True:
            payload = input()
            cmd = payload.split(" ")[0]

            if cmd == "help":
                self.get_help()

            elif cmd in self.commands:
                try:
                    self.clear_extended_command()
                    action = self.commands[cmd]["action"]
                    action(payload=payload, repl=self)

                except CommandSyntaxException as err:
                    self.repl_displayer.display_warning(str(err))

                except APIErrorException as err:
                    self.repl_displayer.display_api_error(err)

                except Exception as err:
                    self.repl_displayer.display_error(str(err))

            elif cmd in self.extended_commands:
                try:
                    action = self.extended_commands[cmd]
                    action(payload=payload, repl=self)

                except APIErrorException as err:
                    self.repl_displayer.display_api_error(err)

                except Exception as err:
                    self.repl_displayer.display_error(str(err))

            else:
                self.repl_displayer.display_warning("Command not found")

            if single_command:
                break

            self._show_prompt()
