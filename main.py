import speech_recognition as sr
from selenium import webdriver
import time

PATH = "/Users/mrjello/Downloads/chromedriver"
USERPATH = "--user-data-dir=/Users/mrjello/Desktop/CSE-Projects/VoiceAssistance/UserData"

op = webdriver.ChromeOptions()
op.add_argument(USERPATH)
#op.add_argument('--headless')
op.add_experimental_option("excludeSwitches", ["enable-automation"])
op.add_experimental_option('useAutomationExtension', False)
op.page_load_strategy = 'normal'

recognizer = sr.Recognizer()

while True:
    try:
        with sr.Microphone() as mic:
            recognizer.adjust_for_ambient_noise(mic, duration=0.2)
            audio = recognizer.listen(mic)
            text = recognizer.recognize_google(audio)
            text = text.lower()
            print(text)

            if(text == "open youtube"):
                driver = webdriver.Chrome(PATH, options=op)
                driver.get('https://www.youtube.com/')
                time.sleep(5)

    except sr.UnknownValueError():
        recognizer = sr.Recognizer()
        continue
