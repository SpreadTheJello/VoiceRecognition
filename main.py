import sys
import os
import threading
import json
import speech_recognition as sr
import commands as cmd
from neuralintents import GenericAssistant
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QTextEdit, QPushButton, QLabel, QWidget, QPlainTextEdit
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

#extract the patttern of each command form json file 
with open("command_intents.json") as f:
    command_intents = json.load(f)

# Extract the patterns for each command
command_patterns = {}
for intent in command_intents["intents"]:
    command_patterns[intent["tag"]] = intent["patterns"]


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
    "mute_video": cmd.mute_video(browser),
    "fullscreen": cmd.fullscreen(browser),
    "theater_mode": cmd.theater_mode(browser),
    "stop_listening": cmd.stop_listening(),
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
    # Add a custom signal for processing updates and console output
    processing_signal = pyqtSignal(str)
    console_output_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.init_ui()
        self.listening = False
        # Initialize the lines_count variable
        self.lines_count = 0

    def init_ui(self):
        # Set the window title and size
        self.setWindowTitle("YouTube Voice Control")
        self.setFixedSize(400, 800)
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout(self.central_widget)

        # Add a label and text box to display the console output
        self.console_output = QPlainTextEdit()
        self.console_output.setReadOnly(True)
        layout.addWidget(self.console_output)

        # Add a loading label to show when the app is preparing to listen
        self.loading_label = QLabel("Loading...")
        self.loading_label.setVisible(False)
        layout.addWidget(self.loading_label)

        # Add a label to show the processing status
        self.processing_label = QLabel()
        layout.addWidget(self.processing_label)

        # Add a button to start listening
        self.start_button = QPushButton("Start Listening")
        self.start_button.clicked.connect(self.start_listening)
        layout.addWidget(self.start_button)

        # Shows the microphone status
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")
        self.mic_on = QPixmap(os.path.join(image_path, "mic_on.png"))
        self.mic_off = QPixmap(os.path.join(image_path, "mic_off.png"))
        self.mic_label = QLabel()
        self.mic_label.setPixmap(self.mic_off.scaled(64, 64))
        layout.addWidget(self.mic_label)

        # Add a label and text box to display the available commands
        self.commands_label = QLabel("Available Commands:")
        layout.addWidget(self.commands_label)
        self.commands_text = QPlainTextEdit()
        self.commands_text.setReadOnly(True)
        for command, patterns in command_patterns.items():
            self.commands_text.appendPlainText(f"{patterns[0]}")
        layout.addWidget(self.commands_text)

        # Description of the app
        self.description = QLabel("About our App:")
        layout.addWidget(self.description)
        self.description_text = QPlainTextEdit()
        self.description_text.setReadOnly(True)
        self.description_text.appendPlainText("Greetings User! We are pleased that you are using YouTube Voice control! This app essentially allows you to control YouTube with your own voice. First off, its best to be using this app with a pair of wireless headphones or ear-buds for maximum efficiency of this app. As using this app with loud speakers may impact performance. Once you have your Headphone/ear-buds. Go ahead and click begin to start your app. So after the screen will minimize with a microphone Icon and some speech catch to let you know if you are being heard correctly.")
        layout.addWidget(self.description_text)
        
        # Connect the processing_signal to the update_processing_label function
        self.processing_signal.connect(self.update_processing_label)
        # Connect the console_output_signal to the update_console_output function
        self.console_output_signal.connect(self.update_console_output)

    def update_processing_label(self, text):
        self.processing_label.setText(text)

    def update_console_output(self, text):
        self.console_output.appendPlainText(text)

    # Stop listening when user says "stop listening"
    def stop_listening(self):
        self.listening = False
        self.start_button.setText("Start Listening")
        self.console_output.append("\nStopped Listening...")

    def listen(self):
        while self.listening:
            # Show the loading label and disable button and process events
            self.start_button.setEnabled(False)
            self.loading_label.setVisible(True)
            QApplication.processEvents()
            
            # Listen for audio
            with sr.Microphone(device_index=1) as mic:
                r.adjust_for_ambient_noise(mic)
                # Hide the loading label and process events
                self.loading_label.setVisible(False)
                self.start_button.setEnabled(True)
                QApplication.processEvents()
                
                # Show the listening message
                self.console_output_signal.emit("\nListening...")
                self.mic_label.setPixmap(self.mic_on.scaled(64, 64))
                QApplication.processEvents()
                audio = r.listen(mic, phrase_time_limit=4)
            
            # Update the lines_count
            self.lines_count += 1

            if self.lines_count > 3:
                # Clear the console_output
                self.console_output.clear()
                self.lines_count = 1  # Reset the lines_count to 1, as the next line will be added immediately

            # Show the processing command message
            self.processing_signal.emit("Processing Command...")
            QApplication.processEvents()

            # Change the mic image to off
            self.mic_label.setPixmap(self.mic_off.scaled(64, 64))
            QApplication.processEvents()

            # Attempt to recognize the audio
            try:
                input = r.recognize_google(audio)
                input = input.lower()
                if input == "stop listening":
                    self.stop_listening()
                    break
                response = assistant.request(input)
                if response != "I don't know how to handle that command": 
                    self.console_output_signal.emit("You said: " + input)
                else:
                    self.console_output_signal.emit("Command not recognized")

            # Handle errors
            except sr.UnknownValueError:
                self.console_output_signal.emit("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                self.console_output_signal.emit("Could not request results from Google Speech Recognition service; {0}".format(e))

            # Clear the processing command message
            self.processing_signal.emit("")
            QApplication.processEvents()

    # Function to start/stop listening
    def start_listening(self):
        if not self.listening:
            self.listening = True
            self.start_button.setText("Stop Listening")
            self.processing_signal.emit("")
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
