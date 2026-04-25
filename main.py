from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout

import speech_recognition as sr
import pyttsx3
import webbrowser
import time
import threading
import os

# Voice setup
engine = pyttsx3.init()
engine.setProperty('rate', 150)

recognizer = sr.Recognizer()

FILE_NAME = "names.txt"
names_list = []

def speak(text):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()

def listen():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        return recognizer.recognize_google(audio).lower()
    except:
        return ""

# 🔹 Load or ask first name
def load_names():
    global names_list

    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as f:
            names_list = [name.strip() for name in f.readlines()]
    else:
        speak("Tell me your name")
        name = listen()

        if name:
            names_list.append(name)
            with open(FILE_NAME, "w") as f:
                f.write(name)
            speak(f"Hello {name}")
        else:
            names_list.append("friend")

# 🔹 Detect wake word
def detect_wake_word(command):
    for name in names_list:
        if f"hey {name.lower()}" in command:
            return name
    return None

# 🔹 Execute commands
def execute(command, active_name):

    if "open youtube" in command:
        speak(f"Opening YouTube {active_name}")
        webbrowser.open("https://youtube.com")

    elif "open google" in command:
        speak(f"Opening Google {active_name}")
        webbrowser.open("https://google.com")

    elif "open whatsapp" in command:
        speak(f"Opening WhatsApp {active_name}")
        webbrowser.open("https://web.whatsapp.com")

    elif "time" in command:
        speak(f"{active_name}, time is " + time.strftime("%H:%M"))

    elif "add name" in command:
        speak("Tell new name")
        new_name = listen()
        if new_name:
            names_list.append(new_name)
            with open(FILE_NAME, "a") as f:
                f.write("\n" + new_name)
            speak(f"{new_name} added successfully")

    elif "what can you do" in command:
        speak(f"I can open apps, tell time, and help you {active_name}")

    else:
        speak(f"Sorry {active_name}, I did not understand")

# 🔹 Always listening loop
def assistant_loop(label):
    load_names()
    speak("Sagar Assistant is ready")

    while True:
        command = listen()

        if command:
            label.text = "Heard: " + command

            name = detect_wake_word(command)

            if name:
                speak(f"Yes {name}, tell me")
                command = listen()
                execute(command, name)

# 🔹 App UI
class SagarAssistantApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')

        self.label = Label(
            text="Assistant is always listening...",
            font_size=20
        )

        layout.add_widget(self.label)

        # Auto start assistant
        threading.Thread(target=assistant_loop, args=(self.label,), daemon=True).start()

        return layout

if __name__ == "__main__":
    SagarAssistantApp().run()