import speech_recognition as sr
import commands as cmd
from neuralintents import GenericAssistant
from selenium import webdriver

driver_path = "/path/to/chromedriver"


browser = webdriver.Chrome(driver_path)

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

assistant = GenericAssistant('command_intents.json', intent_methods=mappings)
# assistant.train_model()
# assistant.save_model()
assistant.load_model()

# use microphone 1 as the audio source

# print("Available microphones:")
# for index, name in enumerate(sr.Microphone.list_microphone_names()):
#     print(f"Index: {index}, Name: {name}")

# channel = int(input("Enter the index of the desired microphone: "))

r = sr.Recognizer()

while True:
    with sr.Microphone(device_index=1) as mic:
        r.adjust_for_ambient_noise(mic)
        print("\nListening...")
        audio = r.listen(mic, phrase_time_limit=4)

    try:
        input = r.recognize_google(audio)
        input = input.lower()
        response = assistant.request(input)
        if response != "I don't know how to handle that command":
            print("You said: " + input)
        else:
            print("Command not recognized")

    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
