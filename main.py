import speech_recognition as sr
import commands as cmd
from neuralintents import GenericAssistant

channel = 13
mappings = {
    "open_youtube": cmd.open_youtube,
    "play_pause": cmd.play_pause,
    "newtab": cmd.newtab,
    "open_youtube_newtab": cmd.open_youtube_newtab,
    "homepage_random_video": cmd.homepage_random_video,
    "next_video": cmd.next_video,
    "homepage": cmd.homepage,
    "back_button": cmd.back_button,
    "forward_button": cmd.forward_button
}

assistant = GenericAssistant('command_intents.json', intent_methods=mappings)
#assistant.train_model()
#assistant.save_model()
assistant.load_model()

for index, name in enumerate(sr.Microphone.list_microphone_names()):
        if "pulse" in name:
            channel = index

        r = sr.Recognizer()

        with sr.Microphone(device_index=channel) as mic:
            r.adjust_for_ambient_noise(mic)
            print("\nListening...")
            audio = r.listen(mic, phrase_time_limit=4)

        try:
            input = r.recognize_google(audio)
            input = input.lower()
            assistant.request(input)
            print("You said: " + input)
            #cmd.run(input)

        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
