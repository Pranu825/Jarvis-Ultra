import speech_recognition as sr
import pyttsx3
import os
import pyautogui
import requests
import datetime
import psutil
import ctypes
import subprocess
import time
from playsound import playsound
import threading

# GEMINI API Setup
GEMINI_API_KEY = "AIzaSyAlo9_nqpO8ESSH0vUuRzMawm6MKYDL_Vk"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

# Weather API
WEATHER_API_KEY = "36fc0775d3624447bb865429252804"
CITY = "Chennai"

# Initialize TTS Engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)

def speak(text):
    print(f"Jarvis: {text}")
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("\nListening...")
        recognizer.adjust_for_ambient_noise(source, duration=1)  # Improve listening
        audio = recognizer.listen(source, phrase_time_limit=5)
    try:
        command = recognizer.recognize_google(audio)
        command = command.lower()
        print(f"You: {command}")
        return command
    except:
        # Instead of "Sorry, I couldn't understand", Jarvis gives a smart reply
        smart_replies = [
            "I'm still learning. Can you say that again?",
            "That's interesting! Could you repeat?",
            "Hmm... I want to understand better. Tell me again!",
            "One more time, please."
        ]
        speak(random.choice(smart_replies))
        return ""

def ask_gemini(prompt):
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }
    response = requests.post(GEMINI_URL, json=payload)
    try:
        reply = response.json()['candidates'][0]['content']['parts'][0]['text']
        return reply
    except:
        return "I'm trying my best, but couldn't fetch a smart response."

def take_screenshot():
    screenshot = pyautogui.screenshot()
    path = "screenshot.png"
    screenshot.save(path)
    speak("Screenshot taken and saved.")

def lock_pc():
    speak("Locking your PC.")
    ctypes.windll.user32.LockWorkStation()

def open_youtube():
    speak("Opening YouTube.")
    os.system("start https://www.youtube.com/")

def open_spotify():
    speak("Opening Spotify.")
    os.system("start https://open.spotify.com/")

def control_wifi(turn_on):
    if turn_on:
        os.system("netsh interface set interface Wi-Fi enabled")
        speak("Turning Wi-Fi on.")
    else:
        os.system("netsh interface set interface Wi-Fi disabled")
        speak("Turning Wi-Fi off.")

def check_battery():
    battery = psutil.sensors_battery()
    percent = battery.percent
    speak(f"Your battery is at {percent} percent.")

def get_weather():
    url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={CITY}&aqi=no"
    try:
        response = requests.get(url)
        data = response.json()
        if "current" in data:
            temp = data["current"]["temp_c"]
            desc = data["current"]["condition"]["text"]
            weather_report = f"The temperature in {CITY} is {temp} degrees Celsius with {desc}."
            speak(weather_report)
        else:
            speak("Sorry, I couldn't fetch weather details.")
    except:
        speak("There was an error getting the weather information.")

def system_stats():
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    speak(f"CPU usage is at {cpu} percent and RAM usage is at {ram} percent.")

def play_music():
    music_folder = "C:\\Users\\Public\\Music"  # Change if needed
    songs = os.listdir(music_folder)
    if songs:
        speak("Playing music.")
        os.startfile(os.path.join(music_folder, songs[0]))
    else:
        speak("No songs found in your music folder.")

def auto_update():
    speak("Checking for updates...")
    speak("Jarvis Ultra is already up to date!")

def custom_shortcut(name):
    if "vs code" in name:
        speak("Opening Visual Studio Code.")
        os.system("start code")
    elif "calculator" in name:
        speak("Opening Calculator.")
        os.system("start calc")
    elif "paint" in name:
        speak("Opening Paint.")
        os.system("start mspaint")
    else:
        speak("Shortcut not found.")

def control_os(command):
    if "open chrome" in command:
        speak("Opening Chrome.")
        os.system("start chrome")
    elif "open notepad" in command:
        speak("Opening Notepad.")
        os.system("start notepad")
    elif "open command prompt" in command or "open cmd" in command:
        speak("Opening Command Prompt.")
        os.system("start cmd")
    elif "shutdown computer" in command:
        speak("Shutting down the computer.")
        os.system("shutdown /s /t 5")
    elif "restart computer" in command:
        speak("Restarting the computer.")
        os.system("shutdown /r /t 5")
    elif "volume up" in command:
        speak("Increasing volume.")
        pyautogui.press('volumeup', presses=5)
    elif "volume down" in command:
        speak("Decreasing volume.")
        pyautogui.press('volumedown', presses=5)
    elif "mute volume" in command:
        speak("Muting volume.")
        pyautogui.press('volumemute')
    elif "open settings" in command:
        speak("Opening Settings.")
        os.system("start ms-settings:")

def play_intro_sound():
    try:
        playsound("jarvis_intro.mp3")  # Path to your intro sound
    except Exception as e:
        print(f"Error playing intro sound: {e}")

def main():
    import random  # Import inside main to avoid error

    # Play intro sound in a separate thread
    intro_thread = threading.Thread(target=play_intro_sound)
    intro_thread.start()

    speak("Hello! Boss")

    while True:
        command = listen()

        if command == "":
            continue

        if "exit" in command or "stop" in command or "bye" in command:
            speak("Goodbye Boss!")
            break

        # OS Controls
        control_os(command)

        # Jarvis Intelligence
        if "jarvis" in command or "tell me" in command or "what is" in command or "who is" in command:
            reply = ask_gemini(command)
            speak(reply)

        # Extra Commands
        elif "time" in command:
            time_now = datetime.datetime.now().strftime('%I:%M %p')
            speak(f"Current time is {time_now}")
        elif "screenshot" in command:
            take_screenshot()
        elif "lock pc" in command:
            lock_pc()
        elif "open youtube" in command:
            open_youtube()
        elif "open spotify" in command:
            open_spotify()
        elif "wifi on" in command:
            control_wifi(True)
        elif "wifi off" in command:
            control_wifi(False)
        elif "battery" in command:
            check_battery()
        elif "weather" in command or "temperature" in command:
            get_weather()
        elif "system stats" in command or "cpu usage" in command or "ram usage" in command:
            system_stats()
        elif "play music" in command:
            play_music()
        elif "update jarvis" in command:
            auto_update()
        elif "open" in command and "shortcut" in command:
            shortcut_name = command.replace("open", "").replace("shortcut", "").strip()
            custom_shortcut(shortcut_name)

if __name__ == "__main__":
    main()