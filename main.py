import speech_recognition as sr
import commands as cmd
from neuralintents import GenericAssistant
from selenium import webdriver

# Path to the ChromeDriver executable
driver_path = "/path/to/chromedriver"

# Create a browser instance using the ChromeDriver
browser = webdriver.Chrome(driver_path)

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

# Continuous voice command processing loop
while True:
    with sr.Microphone(device_index=1) as mic:
        # Adjust for ambient noise
        r.adjust_for_ambient_noise(mic)
        print("\nListening...")
        # Record audio for 4 seconds
        audio = r.listen(mic, phrase_time_limit=4)

    try:
        # Recognize speech using Google Speech Recognition
        input = r.recognize_google(audio)
        input = input.lower()
        # Get the response from the assistant
        response = assistant.request(input)
        if response != "I don't know how to handle that command":
            print("You said: " + input)
        else:
            print("Command not recognized")

    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
