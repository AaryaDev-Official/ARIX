import os
import requests
import webbrowser
import platform
import subprocess
from datetime import datetime
from config import Config

class ArixTools:
    @staticmethod
    def get_time():
        """Returns the current time in a friendly format."""
        return datetime.now().strftime("%I:%M %p")

    @staticmethod
    def get_date():
        """Returns today's date."""
        return datetime.now().strftime("%A, %B %d, %Y")

    @staticmethod
    def open_site(domain):
        """Opens any website (e.g., 'google.com')."""
        webbrowser.open(f"https://{domain}")
        return f"Opening {domain} now."

    @staticmethod
    def system_info():
        """Returns basic OS details."""
        details = f"Running on {platform.system()} {platform.release()}"
        return details

    @staticmethod
    def launch_app(app_name):
        """Launches common apps (Windows focus)."""
        apps = {
            "notepad": "notepad.exe",
            "calculator": "calc.exe",
            "chrome": "chrome.exe"
        }
        if app_name in apps:
            subprocess.Popen(apps[app_name])
            return f"Launching {app_name}."
        return "Application path not found in my database."
    
    @staticmethod
    def get_weather(city):
        try:
            import requests
            url = f"https://wttr.in/{city}?format=%C+%t"
            return f"It is {requests.get(url, timeout=5).text} in {city}."
        except Exception:
            return f"Weather services are unavaiable, You are offline, {Config.USER_NAME}"
        
    @staticmethod
    def set_volume(level):
        try:
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))
            volume.SetMasterVolumeLevelScalar(int(level) / 100, None)
            return f"System volume adjusted to {level} percent."
        except Exception as e:
            return "I was unable to modify the system volume levels."
        
    @staticmethod
    def play_music(song_name):
        try:
            import pywhatkit
            pywhatkit.playonyt(song_name)
            return f"Playing {song_name} for you, {Config.USER_NAME}."
        except Exception:
            return "I need an internet connection for specific songs."