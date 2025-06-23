"""
Assist - Configuration settings
"""

# Application settings
APP_NAME = "Assist"
APP_VERSION = "0.1.0"
DEBUG_MODE = True

# UI settings
UI_THEME = "dark"  # "light" or "dark"
POPUP_WIDTH = 600
POPUP_HEIGHT = 200
POPUP_OPACITY = 0.9
SHOW_SIDE_PANEL = True
SIDE_PANEL_WIDTH = 300

# Voice recognition settings
WAKE_WORD = "assist"  # Wake word to activate the assistant
VOICE_TIMEOUT = 5.0  # Seconds of silence before stopping listening
LANGUAGE = "en-US"  # Language for speech recognition

# AI provider settings
AI_PROVIDER = "qwen"  # "qwen", "openai", or "mock" for testing
QWEN_API_KEY = ""  # Your Qwen API key
OPENAI_API_KEY = "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"
AI_PROVIDER = "openai"
YOUTUBE_API_KEY = "AIzaSyDAaHpi9pM9suw9yMSjoRhShxPHOe9mBJA"

# Self-Operating-Computer settings
SOC_ENABLED = True
SOC_PATH = ""  # Path to Self-Operating-Computer installation

# System settings
ALLOWED_APPLICATIONS = [
    "notepad.exe",
    "calc.exe",
    "explorer.exe",
    "chrome.exe",
    "firefox.exe",
    "code.exe",
    "excel.exe",
    "powerpnt.exe",
]