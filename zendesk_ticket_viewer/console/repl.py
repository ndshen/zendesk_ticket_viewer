from typing import Callable

from console.commands import CommandSyntaxException
from console.display import display_api_error, display_warning, display_error
from api.ticket_service import APIErrorException


class Repl:
    prompt = "zendesk> "
    welcome_prompt = "Welcome to zendesk ticket viewer. Type 'help' to see all the commands or 'quit' to exit the program."

    def __init__(self, is_show_prompt=True) -> None:
        self.is_show_prompt = is_show_prompt
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
            print(f"{indent}{key}: {val['help']}")
        
    def _show_prompt(self) -> None:
        if self.is_show_prompt:
            print(self.prompt, end="")
    
    def run(self) -> None:
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
                    display_warning(str(err))
                
                except APIErrorException as err:
                    display_api_error(err)

                except Exception as err:
                    display_error(str(err))
            
            elif cmd in self.extended_commands:
                try:
                    action = self.extended_commands[cmd]
                    action(payload=payload, repl=self)

                except APIErrorException as err:
                    display_api_error(err)

                except Exception as err:
                    display_error(str(err))
            
            else:
                display_warning("Command not found")

            self._show_prompt()

