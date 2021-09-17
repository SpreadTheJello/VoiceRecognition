from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import Key, Controller as KeyboardController
import time

mouse = MouseController()
keyboard = KeyboardController()

def click():
    time.sleep(0.1)
    mouse.click(Button.left, 1)

def open_youtube():
    mouse.position = (40, 115)
    click()
    print("--opened youtube--")

def play_pause():
    mouse.position = (32, 884)
    click()

def newtab():
    keyboard.press(Key.cmd)
    keyboard.press('t')
    keyboard.release(Key.cmd)
    keyboard.release('t')
    print("--opened new tab--")

def open_youtube_newtab():
    keyboard.press(Key.cmd)
    keyboard.press('t')
    keyboard.release(Key.cmd)
    keyboard.release('t')
    mouse.position = (40, 115)
    click()
    print("--opened youtube in new tab--")
    
def homepage_video(num):
    return
