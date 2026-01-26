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



def speak_old(text):
    engine.say(text)
    engine.runAndWait()

def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3') 
    # Load the MP3 file
    pygame.mixer.music.load('temp.mp3')

    # Play the MP3 file
    pygame.mixer.music.play()

    # Keep the program running until the music stops playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    
    pygame.mixer.music.unload()
    os.remove("temp.mp3") 




GROQ_API_KEY = os.getenv("GROQ_API_KEY")   # put your key here

def ask_ai(question):
    client = Groq(api_key=GROQ_API_KEY)

    chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "system", "content": "Give short, simple, and direct answers in 3-4 sentences."},
        {    "role": "user",
            "content": question,
        }
    ],
    model="llama-3.3-70b-versatile",
    )

    return chat_completion.choices[0].message.content


def processcommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musiclibrary.music[song]
        webbrowser.open(link)
    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}")
        if r.status_code == 200:
            # Parse the JSON response
            data = r.json()
            
            # Extract the articles
            articles = data.get('articles', [])
            
            # Print the headlines
            for article in articles:
                print(article['title'])
                time.sleep(0.3) 
                speak(article['title'])

    else:
        # Let OpenAI handle the request
        output = ask_ai(c)
        print(output)
        time.sleep(0.5)
        speak(output)
    
if __name__ == "__main__":
    speak("Initializing Farina...")
    r = sr.Recognizer()

    while True:
        print("recognizing...")
        try:
            with sr.Microphone() as source:
                print("Listening for wake word...")
                audio = r.listen(source, timeout=2, phrase_time_limit=2)
            word = r.recognize_google(audio)

            if "farina" in word.lower():
                speak("Yes")
                with sr.Microphone() as source:
                    print("Farina Active...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)
                    processcommand(command)

        except Exception as e:
            print("Error:", e)
