import speech_recognition as sr
import webbrowser
import pyttsx3
import musiclibrary
from groq import Groq
import requests
import time
from gtts import gTTS
import pygame
import os
from dotenv import load_dotenv

load_dotenv()

pygame.mixer.init()
recognizer = sr.Recognizer()
engine = pyttsx3.init()

newsapi = os.getenv("newsapi")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

running = True


# ---------------- SPEAK FUNCTION ----------------
def speak(text):
    tts = gTTS(text)
    tts.save("temp.mp3")

    pygame.mixer.music.load("temp.mp3")
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.music.unload()
    os.remove("temp.mp3")


# ---------------- AI FUNCTION ----------------
def ask_ai(question):
    client = Groq(api_key=GROQ_API_KEY)

    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system",
             "content": "Give short, simple, and direct answers in 3-4 sentences."},
            {"role": "user", "content": question}
        ],
        model="llama-3.3-70b-versatile",
    )

    return chat_completion.choices[0].message.content


# ---------------- COMMAND PROCESSING ----------------
def processcommand(command, display_callback):
    command = command.lower()

    if "open google" in command:
        webbrowser.open("https://google.com")
        display_callback("FARINA: Opening Google...\n\n")
        speak("Opening Google")

    elif "open facebook" in command:
        webbrowser.open("https://facebook.com")
        display_callback("FARINA: Opening Facebook...\n\n")
        speak("Opening Facebook")

    elif "open youtube" in command:
        webbrowser.open("https://youtube.com")
        display_callback("FARINA: Opening YouTube...\n\n")
        speak("Opening YouTube")

    elif "open linkedin" in command:
        webbrowser.open("https://linkedin.com")
        display_callback("FARINA: Opening LinkedIn...\n\n")
        speak("Opening LinkedIn")

    elif command.startswith("play"):
        song = command.replace("play", "").strip().lower()

        found = False

        for key in musiclibrary.music:
            if key in song.replace(" ", ""):
                webbrowser.open(musiclibrary.music[key])
                display_callback(f"FARINA: Playing {key}\n\n")
                speak(f"Playing {key}")
                found = True
                break

        if not found:
            display_callback("FARINA: Song not found in library.\n\n")
            speak("Song not found in library")

    elif "news" in command:
        display_callback("FARINA: Fetching latest news...\n\n")
        speak("Fetching latest news")

        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}")

        if r.status_code == 200:
            data = r.json()
            articles = data.get("articles", [])[:6]

            for article in articles:
                headline = article["title"]
                display_callback("News: " + headline + "\n\n")
                speak(headline)
                time.sleep(0.5)

    else:
        output = ask_ai(command)
        display_callback("FARINA: " + output + "\n\n")
        speak(output)


# ---------------- MAIN ASSISTANT LOOP ----------------
def start_assistant(display_callback):
    global running
    running = True

    speak("Initializing Farina")
    display_callback("FARINA Initialized...\n\n")

    r = sr.Recognizer()

    while running:
        try:
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source, duration=0.5)
                audio = r.listen(source)

            word = r.recognize_google(audio)
            # display_callback("Heard: " + word + "\n\n")

            if "farina" in word.lower():
                speak("Yes")
                display_callback("Wake word detected...\n\n")

                with sr.Microphone() as source:
                    audio = r.listen(source)
                    command = r.recognize_google(audio)

                    display_callback("You: " + command + "\n\n")
                    processcommand(command, display_callback)

        except Exception:
            continue


def stop_assistant():
    global running
    running = False
    speak("Stopping assistant")