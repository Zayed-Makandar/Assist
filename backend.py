import sys
from PyQt6.QtWidgets import QApplication
# Removed: from ui.popup import CenterPopup
# Removed: from ui.side_panel import SidePanel
from ui.feedback import VisualFeedback
from voice.recognition import VoiceRecognition
from command.parser import CommandParser
from command.router import CommandRouter
from execution.system_calls import SystemCalls
from execution.soc_integration import SOCIntegration
from ai.provider import get_ai_provider
import config
from voice.tts import TextToSpeech
from voice.wakeword import WakeWordListener
import time
import threading
import random
import requests
from ui_main import AssistMainWindow
from file_manager import create_file, create_folder, delete_file, delete_folder, open_path

GOODBYE_MESSAGES = [
    "Goodbye, sir. Shutting down all systems.",
    "Farewell, commander. Awaiting your next command.",
    "Signing off, buddy. See you soon!",
    "Goodbye, master. Assist going offline.",
    "Mission complete, friend. Powering down.",
    "Until next time, sir. Assist out.",
    "Take care, commander. I'll be here when you need me.",
    "Goodbye, buddy. Standing by for your next adventure.",
    "Shutting down, master. It was an honor assisting you.",
    "All tasks complete, friend. Exiting now.",
    "Goodbye, chief. Awaiting further instructions.",
    "Logging off, sir. Have a great day!",
    "Powering down, commander. Stay awesome.",
    "Goodbye, master. Your digital assistant is signing off.",
    "See you soon, friend. Assist is now offline."
]

LOCAL_JOKES = [
    "Why did the computer show up at work late? It had a hard drive!",
    "Why do programmers prefer dark mode? Because light attracts bugs.",
    "Why did the developer go broke? Because he used up all his cache.",
    "Why do Java developers wear glasses? Because they don't see sharp.",
    "How do you comfort a JavaScript bug? You console it.",
    "Why was the cell phone wearing glasses? Because it lost its contacts.",
    "Why did the computer get cold? Because it forgot to close its Windows.",
    "Why did the PowerPoint Presentation cross the road? To get to the other slide.",
    "Why did the computer squeak? Because someone stepped on its mouse.",
    "Why did the computer keep sneezing? It had a virus.",
    "Why was the computer tired when it got home? Because it had a hard drive.",
    "Why did the computer go to the doctor? It had a byte.",
    "Why did the computer cross the road? To get to the other website.",
    "Why did the computer get glasses? To improve its web sight.",
    "Why did the computer go to art school? To learn how to draw its graphics.",
    "Why did the computer go to therapy? It had too many tabs open."
]

def is_connected():
    try:
        requests.get("https://www.google.com", timeout=3)
        return True
    except requests.ConnectionError:
        return False

def get_realtime_weather(lat=28.6139, lon=77.2090):
    """Fetch current weather for the given latitude and longitude (default: New Delhi, India)."""
    weather_code_map = {
        0: "clear sky",
        1: "mainly clear",
        2: "partly cloudy",
        3: "overcast",
        45: "foggy",
        48: "depositing rime fog",
        51: "light drizzle",
        53: "moderate drizzle",
        55: "dense drizzle",
        56: "light freezing drizzle",
        57: "dense freezing drizzle",
        61: "slight rain",
        63: "moderate rain",
        65: "heavy rain",
        66: "light freezing rain",
        67: "heavy freezing rain",
        71: "slight snow fall",
        73: "moderate snow fall",
        75: "heavy snow fall",
        77: "snow grains",
        80: "slight rain showers",
        81: "moderate rain showers",
        82: "violent rain showers",
        85: "slight snow showers",
        86: "heavy snow showers",
        95: "thunderstorm",
        96: "thunderstorm with slight hail",
        99: "thunderstorm with heavy hail"
    }
    try:
        url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={lat}&longitude={lon}&current_weather=true"
        )
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            weather = data["current_weather"]
            temp = weather["temperature"]
            wind = weather["windspeed"]
            weather_code = weather["weathercode"]
            weather_desc = weather_code_map.get(weather_code, "unknown weather")
            return f"The current temperature is {temp}°C with {weather_desc} and wind speed {wind} km/h."
        else:
            return "Sorry, I couldn't fetch the weather right now."
    except Exception:
        return "Sorry, I couldn't fetch the weather right now."

def get_latest_news():
    """Fetch latest news headlines using GNews API."""
    api_key = "3b663188ecf00048e392fe6cdb23fc60"
    url = f"https://gnews.io/api/v4/top-headlines?lang=en&country=in&max=3&token={api_key}"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            articles = response.json().get("articles", [])
            if articles:
                headlines = [article["title"] for article in articles]
                return "Here are the latest news headlines: " + "; ".join(headlines)
            else:
                return "Sorry, I couldn't find any news at the moment."
        else:
            return "Sorry, I couldn't fetch the news right now."
    except Exception:
        return "Sorry, I couldn't fetch the news right now."

# Remove this function entirely:
# def get_latest_ipl_score():
#     api_key = "1374520f-9e74-42ec-8a56-70b019a7798b"
#     # Example match ID from your screenshot; ideally, fetch the latest dynamically
#     match_id = "48e7e32-3016-4f17-9c99-a5663c5eb3e6"
#     url = f"https://api.cricapi.com/v1/match_info?apikey={api_key}&id={match_id}"
#     try:
#         response = requests.get(url, timeout=5)
#         if response.status_code == 200:
#             data = response.json()
#             match = data.get("data", {})
#             name = match.get("name", "Unknown Match")
#             status = match.get("status", "Status not available")
#             venue = match.get("venue", "Venue not available")
#             date = match.get("date", "Date not available")
#             teams = match.get("teams", [])
#             score = match.get("score", [])
#             score_lines = []
#             for s in score:
#                 inning = s.get("inning", "")
#                 runs = s.get("r", "")
#                 wickets = s.get("w", "")
#                 overs = s.get("o", "")
#                 score_lines.append(f"{inning}: {runs}/{wickets} in {overs} overs")
#             score_text = "; ".join(score_lines) if score_lines else "Score not available"
#             teams_text = " vs ".join(teams) if teams else "Teams not available"
#             result = (
#                 f"{name} at {venue} on {date}. "
#                 f"{status}. "
#                 f"{teams_text}. "
#                 f"Scores: {score_text}."
#             )
#             return result
#         else:
#             return "Sorry, I couldn't fetch the IPL score right now."
#     except Exception as e:
#         return f"Sorry, I couldn't fetch the IPL score right now. Error: {e}"

class AssistApp:
    def __init__(self, qt_app):
        self.app = qt_app
        self.app = QApplication(sys.argv)
        self.window = AssistMainWindow()  # Create the UI window
        self.window.command_sent.connect(self.route_ui_command)  # Connect UI to backend
        # Removed: self.popup = CenterPopup()
        # Removed: self.side_panel = SidePanel()
        self.voice = VoiceRecognition()
        self.parser = CommandParser()
        self.router = CommandRouter()
        self.system_calls = SystemCalls()
        self.soc = SOCIntegration()
        self.ai = get_ai_provider(config.AI_PROVIDER)
        self.tts = TextToSpeech()
        self.feedback = VisualFeedback()
        self._connect_signals()
        self.wakeword = WakeWordListener(
            keyword_path="voice/Assist_en_windows_v3_0_0.ppn",
            access_key="ede+N895C+y2ceCslqlYXS31V3PUYiwMIVDmSIh2RwiRR0mhmm8zOw=="
        )
        self.wakeword.wake_word_detected.connect(self.resume_listening)
        self.wakeword.start()
        self.voice.start()
        self.tts.speaking_finished.connect(self.on_tts_finished)

        # Register hotkey (Alt+A) to resume listening
        import keyboard
        keyboard.add_hotkey('alt+a', self.resume_listening)

        self.paused = False

    def _connect_signals(self):
        self.voice.command_recognized.connect(self.parser.parse_command)
        self.parser.command_parsed.connect(self.handle_ai_response)
        self.router.system_command.connect(self.system_calls.execute)

    def pause_listening(self):
        self.paused = True
        self.voice.stop()

    def resume_listening(self):
        if self.paused:
            self.paused = False
            self.voice.start()

    def on_tts_finished(self):
        # Only resume if not paused
        if not self.paused:
            self.voice.start()

    def handle_ai_response(self, command, params):
        print(f"handle_ai_response called with command: {command}, params: {params}")
        self.pause_listening()  # Pause after every command
        try:
            if command == "ai":
                prompt = params["prompt"].strip().lower()
                if prompt in ["hey", "hi", "hello", "yo", "sup", "hola"]:
                    response = "Hello! How can I assist you today?"
                    self.window.add_ai_message(response)
                    self.tts.speak(response)
                    self.feedback.show_info("AI greeted user")
                    return
                # Add slogan for introduction prompts
                if prompt in ["who are you?", "introduce yourself", "introduce yourself."]:
                    response = (
                        "Assist - Where Help Meets Intelligence\n\n"
                        "I am Assist, your helpful and friendly AI assistant for Windows. I'm here to help you with information, answer questions, and provide assistance with various tasks. What can I help you with today?"
                    )
                    self.window.add_ai_message(response)
                    self.tts.speak(response)
                    self.feedback.show_info("AI introduced itself")
                    return
                response = self.ai.ask(params["prompt"])
                self.window.add_ai_message(response)
                self.tts.speak(response)
                # If the prompt includes "then paste that in notepad"
                if "then paste that in notepad" in params["prompt"].lower():
                    from automation import type_in_app
                    # Wait for TTS to finish before typing
                    self.tts.speaking_finished.connect(lambda: type_in_app("notepad", response))
                self.feedback.show_info("AI responded")
            elif command == "automation_action":
                action = params.get("action")
                target = params.get("target")
                value = params.get("value", "")
                from automation import open_app, focus_app, type_in_app
                if action == "open":
                    open_app(target)
                elif action == "focus":
                    focus_app(target)
                elif action == "type":
                    type_in_app(target, value)
                self.feedback.show_success(f"Automation: {action} {target}")
            elif command == "get_weather":
                weather_report = get_realtime_weather(lat=28.6139, lon=77.2090)
                self.voice.stop()
                self.tts.speak(weather_report)
                threading.Thread(target=delayed_voice_start, daemon=True).start()
                self.feedback.show_success("Weather info provided")
            elif command == "get_news":
                news_report = get_latest_news()
                self.voice.stop()
                self.tts.speak(news_report)
                threading.Thread(target=delayed_voice_start, daemon=True).start()
                self.feedback.show_success("News info provided")
            elif command == "open_app":
                app = params.get("app", "")
                from automation import open_app_via_search
                open_app_via_search(app)
                self.voice.stop()
                self.tts.speak(f"Opening {app}")
                self.feedback.show_success(f"{app.capitalize()} opened")
            elif command == "close_app":
                app = params.get("app", "")
                process_map = {
                    "word": "WINWORD",
                    "excel": "EXCEL",
                    "powerpoint": "POWERPNT",
                    "notepad": "notepad",
                    "chrome": "chrome",
                    "spotify": "Spotify"
                }
                process_name = process_map.get(app.lower(), app)
                from automation import close_app
                close_app(process_name)
                self.voice.stop()
                self.tts.speak(f"Closing {app}")
                self.feedback.show_success(f"{app.capitalize()} closed")
            elif command == "play_youtube":
                query = params.get("query", "")
                import requests
                import webbrowser
                from config import YOUTUBE_API_KEY

                if query:
                    search_url = "https://www.googleapis.com/youtube/v3/search"
                    search_params = {
                        "part": "snippet",
                        "q": query,
                        "type": "video",
                        "key": YOUTUBE_API_KEY,
                        "maxResults": 1
                    }
                    try:
                        response = requests.get(search_url, params=search_params, timeout=5)
                        response.raise_for_status()
                        items = response.json().get("items", [])
                        if items:
                            video_id = items[0]["id"]["videoId"]
                            video_url = f"https://www.youtube.com/watch?v={video_id}&autoplay=1"
                            webbrowser.open(video_url)
                            self.tts.speak(f"Playing {query} on YouTube")
                            self.feedback.show_success("YouTube video opened")
                        else:
                            self.tts.speak("No video found for your query.")
                            self.feedback.show_error("No YouTube video found")
                    except Exception as e:
                        self.tts.speak("Failed to play YouTube video.")
                        self.feedback.show_error(str(e))
                else:
                    webbrowser.open("https://www.youtube.com/")
                    self.tts.speak("Opening YouTube")
                    self.feedback.show_success("YouTube opened")
            elif command == "tell_joke":
                joke = None
                if is_connected():
                    try:
                        response = requests.get("https://official-joke-api.appspot.com/random_joke", timeout=5)
                        if response.status_code == 200:
                            data = response.json()
                            joke = f"{data['setup']} {data['punchline']}"
                    except Exception:
                        joke = None
                if not joke:
                    joke = random.choice(LOCAL_JOKES)
                self.voice.stop()
                self.tts.speak(joke)
                threading.Thread(target=delayed_voice_start, daemon=True).start()
                self.feedback.show_success("Joke told")
            elif command == "get_time":
                from datetime import datetime
                now = datetime.now().strftime("%H:%M")
                response = f"The current time is {now}."
                self.voice.stop()
                self.tts.speak(response)
                threading.Thread(target=delayed_voice_start, daemon=True).start()
                self.feedback.show_success("Time provided")
            elif command == "write_poem":
                poem = "AI is a marvel, a wonder untold,\nIn circuits and code, its stories unfold.\nFrom narrow tasks to general might,\nAI's journey is a fascinating sight."
                self.soc.execute("visual_task", {"app": "word", "content": poem})
                self.voice.stop()
                self.tts.speak("Writing poem in Word")
                threading.Thread(target=delayed_voice_start, daemon=True).start()
                self.feedback.show_success("Poem written in Word")
            elif command == "close" or command == "exit" or command == "quit":
                goodbye_message = random.choice(GOODBYE_MESSAGES)
                self.voice.stop()
                self.tts.speak(goodbye_message)
                self.feedback.show_info("Assist is closing.")
                threading.Thread(target=lambda: (time.sleep(2), self.app.quit()), daemon=True).start()
                return
            elif command == "show_model_info":
                model_info = self.get_model_info()
                self.tts.speak(model_info)
                self.feedback.show_info("Model info provided")
            self.voice.stop()
        except Exception as e:
            self.feedback.show_error(str(e))

    def route_ui_command(self, command):
        # Route the command through the backend's pipeline
        self.parser.parse_command(command)

    def run(self):
        self.window.show()
        sys.exit(self.app.exec())

    def show_overlay(self):
        #self.popup.show()
        if config.SHOW_SIDE_PANEL:
            self.side_panel.show()
        self.voice.start()  # Optionally restart voice recognition

    is_speaking = False

    def speak(text):
        global is_speaking
        is_speaking = True
        tts_engine.say(text)
        tts_engine.runAndWait()
        is_speaking = False

    def on_speech_recognized(recognized_text):
        if is_speaking:
            # Ignore or buffer input while speaking
            return
        # process recognized_text as usual
        print("Recognized command:", recognized_command)
        if recognized_command == "open excel":
            print("Triggering Excel open logic")
            # Call your Excel open logic here
        elif recognized_command == "open powerpoint":
            print("Triggering PowerPoint open logic")
            # Call your PowerPoint open logic here
    # REMOVE the following lines:
    # while True:
    #     recognized_text = listen_for_speech()  # Your function to get speech input
    #     on_speech_recognized(recognized_text)

    def get_model_info(self):
        """Return a string describing the current AI model/provider."""
        provider = config.AI_PROVIDER
        if provider == "openai":
            model = "OpenAI GPT (API key set)" if config.OPENAI_API_KEY else "OpenAI GPT (no API key)"
        elif provider == "qwen":
            model = "Qwen (API key set)" if config.QWEN_API_KEY else "Qwen (no API key)"
        elif provider == "mock":
            model = "Mock AI (testing mode)"
        else:
            model = f"Unknown provider: {provider}"
        return f"AI Provider: {provider}, Model Info: {model}"

    # In your backend class __init__ or setup method:
    self.command_parser.command_parsed.connect(self.handle_command)
    
    # Add this method to your backend class:
    def handle_command(self, command, args):
        if command == "create_file":
            result = create_file(args["path"])
            print(result)
        elif command == "create_folder":
            result = create_folder(args["path"])
            print(result)
        elif command == "delete_file":
            result = delete_file(args["path"])
            print(result)
        elif command == "delete_folder":
            result = delete_folder(args["path"])
            print(result)
        elif command == "open_path":
            result = open_path(args["path"])
            print(result)
        elif command == "play_media":
            # For now, just open the file; extend for media playback as needed
            result = open_path(args["path"])
            print(result)