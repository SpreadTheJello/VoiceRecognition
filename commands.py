from pynput.mouse import Button, Controller
import time

mouse = Controller()

def click():
    time.sleep(0.1)
    mouse.click(Button.left, 1)

def open_youtube():
    mouse.position = (40, 115)
    click()

def play():
    mouse.position = (32, 884)
    click()
    
def homepage_video(num):
    return
