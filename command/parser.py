from PyQt6.QtCore import QObject, pyqtSignal

class CommandParser(QObject):
    command_parsed = pyqtSignal(str, dict)

    def __init__(self):
        super().__init__()
        self.command_map = {
            "exit": "close",
            "close": "close",
            "close yourself": "close",
            "goodbye": "close",
            "quit": "close",
            "shutdown": "close",
        }

    class CommandParser:
        def parse_command(self, recognized_text):
            text = recognized_text.lower().strip()
            # Handle "open" commands for common apps
            if text.startswith("open "):
                app_name = text[5:].strip()
                # Normalize app names for common Office apps
                app_map = {
                    "powerpoint": "powerpoint",
                    "power point": "powerpoint",
                    "excel": "excel",
                    "word": "word",
                    "notepad": "notepad",
                    "spotify": "spotify",
                    "chrome": "chrome",
                    "firefox": "firefox",
                    "calculator": "calc",
                    "calc": "calc",
                    # Add more mappings as needed
                }
                # Remove spaces and check mapping
                normalized_app = app_map.get(app_name.replace(" ", ""), app_name)
                return "open_app", {"app": normalized_app}
            # Add more intent parsing as needed here...

            # Fallback to AI intent
            return "ai", {"prompt": recognized_text}

    def parse_command(self, text):
        text = text.lower().strip()
        # Add this block for model info
        if "model info" in text or "what model" in text or "which model" in text:
            self.command_parsed.emit("show_model_info", {})
            return
        if text.startswith("open "):
            app = text[len("open "):].strip()
            self.command_parsed.emit("open_app", {"app": app})
            return
        if text.startswith("close "):
            app = text[len("close "):].strip()
            self.command_parsed.emit("close_app", {"app": app})
            return
        # Handle "type ... in notepad" pattern
        if text.startswith("type ") and " in notepad" in text:
            value = text[len("type "):text.index(" in notepad")].strip()
            self.command_parsed.emit("automation_action", {"action": "type", "target": "notepad", "value": value})
            return
        # Handle "open notepad" pattern
        if "open" in text and "notepad" in text:
            self.command_parsed.emit("open_app", {"app": "notepad"})
            return
        for phrase, command in self.command_map.items():
            if phrase in text:
                self.command_parsed.emit(command, {})
                return
        command_lower = text
        if "news" in command_lower or "headline" in command_lower:
            self.command_parsed.emit("get_news", {})
        elif "score" in command_lower or "match result" in command_lower or "who won" in command_lower or "ipl" in command_lower or "cricket" in command_lower:
            self.command_parsed.emit("get_sports_score", {})
        elif "open" in command_lower and "notepad" in command_lower:
            self.command_parsed.emit("open_app", {"app": "notepad"})
        elif "open" in command_lower and "calculator" in command_lower:
            self.command_parsed.emit("open_app", {"app": "calculator"})
        elif "open" in command_lower and "word" in command_lower:
            self.command_parsed.emit("open_app", {"app": "word"})
        elif "open" in command_lower and "spotify" in command_lower:
            self.command_parsed.emit("open_app", {"app": "spotify"})
        elif "open" in command_lower and "youtube" in command_lower:
            self.command_parsed.emit("open_app", {"app": "youtube"})
        elif "play" in command_lower and "spotify" in command_lower:
            # Extract song name
            song = command_lower.split("play",1)[1].split("on spotify")[0].strip()
            self.command_parsed.emit("play_music", {"service": "spotify", "song": song})
        elif "play" in command_lower and "youtube" in command_lower:
            # Extract video name
            video = command_lower.split("play",1)[1].split("on youtube")[0].strip()
            self.command_parsed.emit("play_youtube", {"query": video})
        elif "weather" in command_lower:
            self.command_parsed.emit("get_weather", {})
        elif "joke" in command_lower:
            self.command_parsed.emit("tell_joke", {})
        elif "time" in command_lower:
            self.command_parsed.emit("get_time", {})
        else:
            self.command_parsed.emit("ai", {"prompt": text})  # <-- Fix: use 'text' here
            # File/folder/media management commands
            if text.startswith("create file "):
                path = text[len("create file "):].strip()
                self.command_parsed.emit("create_file", {"path": path})
                return
            if text.startswith("create folder "):
                path = text[len("create folder "):].strip()
                self.command_parsed.emit("create_folder", {"path": path})
                return
            if text.startswith("delete file "):
                path = text[len("delete file "):].strip()
                self.command_parsed.emit("delete_file", {"path": path})
                return
            if text.startswith("delete folder "):
                path = text[len("delete folder "):].strip()
                self.command_parsed.emit("delete_folder", {"path": path})
                return
            if text.startswith("open "):
                path = text[len("open "):].strip()
                self.command_parsed.emit("open_path", {"path": path})
                return
            if text.startswith("play "):
                path = text[len("play "):].strip()
                self.command_parsed.emit("play_media", {"path": path})
                return