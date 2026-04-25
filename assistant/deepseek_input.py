import subprocess
from time import sleep
from typing import Self

from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import Key, Controller as KeyboardController
from pyclip import paste as paste_buffer, clear as clear_buffer

from assistant.utility import locate_on_screen
from assistant.config import settings


class DeepseekInput:
    def __init__(self) -> None:
        self.mouse = MouseController()
        self.keyboard = KeyboardController()
        _ = clear_buffer()

    def _switch_to_desktop(self, tag: int) -> None:
        _ = subprocess.run(
            [
                "awesome-client",
                'awful = require("awful");' + 'local screen = awful.screen.focused();' + f'screen.tags[{tag}]:view_only();'
            ]
        )

    def create_new_chat(self) -> None:
        self._switch_to_desktop(2)
        sleep(1)  # to process the switch
        with self.keyboard.pressed(Key.ctrl):
            self.keyboard.press('j')
            self.keyboard.release('j')
        sleep(1)  # wait for the browser to process it

    def submit_prompt(self, message: str) -> None:
        self.keyboard.type(message)
        self.keyboard.press(Key.enter)
        self.keyboard.release(Key.enter)

    def copy(self) -> str | None:
        button_location = locate_on_screen(settings.COPY_BUTTON)
        if button_location is None:
            return None

        self.mouse.position = (button_location[0] + 10, button_location[1] + 10)
        self.mouse.click(Button.left)

        sleep(1)  # to process the copying
        return str(paste_buffer(text=True))

    def expert_mode(self) -> bool:
        button_location = locate_on_screen(settings.EXPERT_BUTTON)
        if button_location is None:
            return False

        self.mouse.position = (button_location[0] + 10, button_location[1] + 10)
        self.mouse.click(Button.left)

        return True

    def instant_mode(self) -> bool:
        button_location = locate_on_screen(settings.INSTANT_BUTTON)
        if button_location is None:
            return False

        self.mouse.position = (button_location[0] + 10, button_location[1] + 10)
        self.mouse.click(Button.left)

        return True

    def message_field(self) -> bool:
        message_field = locate_on_screen(settings.MESSAGE_FIELD)
        if message_field is None:
            return False

        self.mouse.position = (message_field[0] + 10, message_field[1] + 10)
        self.mouse.click(Button.left)

        return True

    def submit_message_field(self) -> bool:
        submit_button = locate_on_screen(settings.SUBMIT_MESSAGE_BUTTON)
        if submit_button is None:
            return False

        self.mouse.position = (submit_button[0] + 10, submit_button[1] + 10)
        self.mouse.click(Button.left)

        return True

    def __enter__(self) -> Self:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        pass
