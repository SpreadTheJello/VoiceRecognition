import sys
import os
import threading
import speech_recognition as sr
import commands as cmd
from neuralintents import GenericAssistant
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QTextEdit, QPushButton, QLabel, QWidget
from PyQt5.QtGui import QPixmap

# Path to the ChromeDriver executable
driver_path = "/path/to/chromedriver"

# Create a browser instance using the ChromeDriver
browser = webdriver.Chrome(service=Service(driver_path))

# Define the command-to-function mappings
mappings = {
    "open_youtube": cmd.open_youtube(browser),
    "play_pause": cmd.play_pause(browser),
    "homepage_random_video": cmd.homepage_random_video(browser),
    "next_video": cmd.next_video(browser),
    "homepage": cmd.homepage(browser),
    "back_button": cmd.back_button(browser),
    "forward_button": cmd.forward_button(browser),
    "mute_video": cmd.mute_video(browser)
}

# Initialize the assistant with the command intents and the mappings
assistant = GenericAssistant('command_intents.json', intent_methods=mappings)

# Uncomment these when commands are added/removed
# assistant.train_model()
# assistant.save_model()

assistant.load_model()

# Create a recognizer instance
r = sr.Recognizer()

class App(QMainWindow):

    def __init__(self):
        super().__init__()

        self.init_ui()
        self.listening = False

    def init_ui(self):
        self.setWindowTitle("YouTube Voice Control")

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout(self.central_widget)

        self.console_output = QTextEdit()
        self.console_output.setReadOnly(True)
        layout.addWidget(self.console_output)

        self.start_button = QPushButton("Start Listening")
        self.start_button.clicked.connect(self.start_listening)
        layout.addWidget(self.start_button)

        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")
        self.mic_on = QPixmap(os.path.join(image_path, "mic_on.png"))
        self.mic_off = QPixmap(os.path.join(image_path, "mic_off.png"))

        self.mic_label = QLabel()
        self.mic_label.setPixmap(self.mic_off.scaled(64, 64))
        layout.addWidget(self.mic_label)

    def listen(self):
        while self.listening:
            with sr.Microphone(device_index=1) as mic:
                r.adjust_for_ambient_noise(mic)
                self.console_output.append("\nListening...")
                self.mic_label.setPixmap(self.mic_on.scaled(64, 64))
                QApplication.processEvents()
                audio = r.listen(mic, phrase_time_limit=4)

            self.mic_label.setPixmap(self.mic_off.scaled(64, 64))
            QApplication.processEvents()

            try:
                input = r.recognize_google(audio)
                input = input.lower()
                response = assistant.request(input)
                if response != "I don't know how to handle that command":
                    self.console_output.append("You said: " + input)
                else:
                    self.console_output.append("Command not recognized")

            except sr.UnknownValueError:
                self.console_output.append("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                self.console_output.append("Could not request results from Google Speech Recognition service; {0}".format(e))

    def start_listening(self):
        if not self.listening:
            self.listening = True
            self.start_button.setText("Stop Listening")
            self.listen_thread = threading.Thread(target=self.listen)
            self.listen_thread.start()
        else:
            self.listening = False
            self.start_button.setText("Start Listening")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_app = App()
    main_app.show()
    sys.exit(app.exec_())
