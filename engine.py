import speech_recognition as sr
import pyttsx3
import os
from config import Config
from tools import ArixTools
from gui import ArixHUD

class ArixEngine:
    def __init__(self, hud_reference=None):
        self.hud = hud_reference
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 170)
        # Choosing a professional voice
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[1].id) 

        
    def ask_ai(self, question):
        try:
            import google.generativeai as genai
            genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
            self.model = genai.GenerativeModel('gemini')

            promot = f"You are ARIX, a helpful AI assistant. Question: {question}"
            response = self.model.generate_content(promot)
            return response.text
        except Exception:
            return "Internet is not connected in your system, I should control your system and specific commands."
        
    
    def speak(self, text):
        """Assistant speaks and logs to console."""
        print(f"[{Config.BOT_NAME}]: {text}")
        if hasattr(self, 'hud') and self.hud:
            self.hud.update_subtitles(text)
        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self):
        """Automated listening protocol."""
        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.pause_threshold = 1.0
            r.adjust_for_ambient_noise(source, duration=0.5)
            try:
                audio = r.listen(source, timeout=5, phrase_time_limit=5)
                return r.recognize_google(audio, language='en-in').lower()
            except:
                return "none"

    def execute_command(self, query):
        """Automated responses for JARVIS-like feel."""
        if 'hello' in query or 'online' in query:
            return f"Systems are fully operational. Welcome back, {Config.USER_NAME}."
        elif 'open code' in query:
            os.system("code")
            return "Initializing Visual Studio Code environments."
        elif 'time' in query:
            from datetime import datetime
            return f"The current time is {datetime.now().strftime('%I:%M %p')}."
        elif "time" in query:
            return ArixTools.get_time()
        elif "open google" in query:
            return ArixTools.open_site("google.com")
        elif "weather" in query:
            city = os.getenv("CITY", "")
            return ArixTools.get_weather(city)
        elif "volume" in query:
            import re
            numbers = re.findall(r'\d+', query)
            if numbers:
                level = int(numbers[0])
                if 0 <= level <= 100:
                    return ArixTools.set_volume(level)
                else:
                    return "Please provide a volume level between 0 and 100."
            return "What level should I set the volume to?"
        elif "play" in query:
            song = query.replace('play', '').strip()
            return ArixTools.play_music(song)
        else:
            return self.ask_ai(query)
    