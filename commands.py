from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import Key, Controller as KeyboardController
import random
import time

mouse = MouseController()
keyboard = KeyboardController()

def click():
    time.sleep(0.1)
    mouse.click(Button.left, 1)

def open_youtube():
    mouse.position = (40, 115)
    click()
    mouse.position = (10, 145)
    print("--opened youtube--")

def play_pause():
    mouse.position = (32, 884)
    click()
    mouse.position = (32, 915)
    print("--paused/played video--")

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
    open_youtube()
    print("--opened youtube in new tab--")
    
def homepage_random_video():
    x = random.randint(1,4)
    y = random.randint(1,2)
    mouse.position = (x*400, y*350)
    click()
    mouse.position = (32, 915)
    print("--played random video--")

def next_video():
    mouse.position = (76, 884)
    click()
    mouse.position = (76, 915)
    print("--played next video--")

def homepage():
    mouse.position = (85, 162)
    click()
    mouse.position = (10, 145)
    print("--went to homepage--")

def back_button():
    mouse.position = (20, 80)
    click()
    mouse.position = (10, 145)
    print("--back button pressed--")

def forward_button():
    mouse.position = (55, 80)
    click()
    mouse.position = (10, 145)
    print("--front button pressed--")
