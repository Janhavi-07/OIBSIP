import tkinter as tk
from tkinter import ttk, scrolledtext
from PIL import Image, ImageTk
import threading
import datetime
import os
import platform
import requests
import feedparser

import pyttsx3
import speech_recognition as sr
import pyjokes
import webbrowser

# --- TTS
engine = pyttsx3.init()

def speak(text):
    chatbox.insert(tk.END, f"Assistant: {text}\n")
    chatbox.yview(tk.END)
    engine.say(text)
    engine.runAndWait()

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Listening...")
        audio = r.listen(source)
    try:
        query = r.recognize_google(audio, language='en-in')
        chatbox.insert(tk.END, f"You: {query}\n")
        chatbox.yview(tk.END)
        return query.lower()
    except Exception:
        speak("Sorry, I didn't catch that.")
        return ""

# --- Weather, News, Apps, etc.
def get_weather(city):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid=031c792b694b91453ee3ab06262f2541&units=metric"
        response = requests.get(url)
        data = response.json()
        if data.get("cod") != 200:
            speak("City not found.")
            return
        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"].title()
        speak(f"The weather in {city} is {desc} with {temp} degrees Celsius.")
    except:
        speak("Error fetching weather.")

def fetch_news():
    feed_url = "https://news.google.com/rss?hl=en-IN&gl=IN&ceid=IN:en"
    try:
        feed = feedparser.parse(feed_url)
        speak("Top headlines:")
        for entry in feed.entries[:3]:
            speak(entry.title)
    except:
        speak("Failed to get news.")

def open_application(app_name):
    apps = {
        "calculator": "calc",
        "notepad": "notepad",
        "cmd": "cmd",
        "excel": "start excel",
        "word": "start winword",
        "file explorer": "explorer"
    }
    cmd = apps.get(app_name)
    if cmd:
        os.system(cmd)
    else:
        speak(f"I can't open {app_name}")

def handle_command(command):
    if "weather" in command:
        speak("Which city?")
        city = listen()
        if city:
            get_weather(city)
    elif "news" in command or "news headlines" in command or "todays news headlines" in command:
        fetch_news()
    elif "name" in command or "your name" in command:
        speak("My name is Venku-your voice assistant")
    elif "hello" in command or "hi" in command:
        speak("Hello! I'm Venku, your voice assistant. Ready to assist you! ")
    elif "joke" in command:
        speak(pyjokes.get_joke())
    elif "search youtube" in command:
        speak("What to search?")
        query = listen()
        webbrowser.open(f"https://www.youtube.com/results?search_query={query}")
    elif "search" in command:
        speak("What to search?")
        query = listen()
        webbrowser.open(f"https://www.google.com/search?q={query}")
    elif "time" in command:
        speak(f"The time is {datetime.datetime.now().strftime('%H:%M:%S')}")
    elif "date" in command:
        speak(f"Today's date is {datetime.datetime.now().strftime('%B %d, %Y')}")
    elif "day" in command:
        speak(f"Today is {datetime.datetime.now().strftime('%A')}")
    elif "open" in command:
        for app in ["calculator", "notepad", "excel", "word", "cmd", "file explorer"]:
            if app in command:
                open_application(app)
                speak(f"opening {app}")
                return
        speak("I can't open that.")
    elif "exit" in command or "quit" in command:
        speak("Goodbye!")
        root.destroy()
    else:
        speak("Sorry, I didn't get that.")

def run_voice_assistant():
    command = listen()
    if command:
        handle_command(command)

# --- GUI Setup
root = tk.Tk()
root.title("🎙️ Venku - Voice Assistant")
root.geometry("500x500")
root.config(bg="#f6f8fb")

# --- Title
title = tk.Label(root, text="Venku Assistant", font=("Segoe UI", 18, "bold"), bg="#f6f8fb")
title.pack(pady=20)

# --- Chat Display
chatbox = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=15, font=("Segoe UI", 10))
chatbox.pack(pady=10, padx=10)

# --- Load mic icon with Pillow fix
from PIL import Image
resample_filter = getattr(Image, 'Resampling', Image).LANCZOS
mic_img_raw = Image.open("mic_icon.png").resize((40, 40), resample_filter)
mic_img = ImageTk.PhotoImage(mic_img_raw)

# --- Mic Button
mic_button = ttk.Button(root, text="🎤 Start Listening", image=mic_img, compound="left",
                        command=lambda: threading.Thread(target=run_voice_assistant).start())
mic_button.pack(pady=15)

# --- Exit Button
exit_btn = ttk.Button(root, text="❌ Quit", command=lambda: root.destroy())
exit_btn.pack(pady=5)

# --- Launch
speak("Assistant activated. Tap the mic to speak.")
root.mainloop()
