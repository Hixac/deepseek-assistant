import subprocess
import time

from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import Key, Controller as KeyboardController

def press_meta_2():
    print("Executing meta-2")
    _ = subprocess.run(
        [
            "awesome-client",
            'awful = require("awful");' + 'local screen = awful.screen.focused();' + 'screen.tags[2]:view_only();'
        ]
    )
    print("End of executing")


press_meta_2()

mouse = MouseController()
keyboard = KeyboardController()

with keyboard.pressed(Key.ctrl):
    keyboard.press('j')
    keyboard.release('j')


keyboard.type("You're my ide assistant, follow these rules: write only code. Make simple python calculation script.")
keyboard.press(Key.enter)
keyboard.release(Key.enter)
