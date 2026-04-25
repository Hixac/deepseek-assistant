import subprocess
from typing import Self

from pynput.mouse import Controller as MouseController
from pynput.keyboard import Key, Controller as KeyboardController


class DeepseekInput:
    def __init__(self) -> None:
        self.mouse = MouseController()
        self.keyboard = KeyboardController()

    def _switch_to_desktop(self, tag: int) -> None:
        _ = subprocess.run(
            [
                "awesome-client",
                'awful = require("awful");' + 'local screen = awful.screen.focused();' + f'screen.tags[{tag}]:view_only();'
            ]
        )

    def create_new_chat(self) -> None:
        self._switch_to_desktop(2)
        with self.keyboard.pressed(Key.ctrl):
            self.keyboard.press('j')
            self.keyboard.release('j')

    def submit_prompt(self, message: str) -> None:
        self.keyboard.type(message)
        self.keyboard.press(Key.enter)
        self.keyboard.release(Key.enter)

    def __enter__(self) -> Self:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        pass
