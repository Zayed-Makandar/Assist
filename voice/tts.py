import pyttsx3
from PyQt6.QtCore import pyqtSignal, QObject

class TextToSpeech(QObject):
    speaking_finished = pyqtSignal()

    def __init__(self, voice_id=None, rate=200):
        super().__init__()  # <-- This line is required!
        self.engine = pyttsx3.init()
        voices = self.engine.getProperty('voices')
        if voice_id is not None:
            self.engine.setProperty('voice', voices[voice_id].id)
        self.engine.setProperty('rate', rate)

    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()
        # After speaking is done:
        self.speaking_finished.emit()

    def list_voices(self):
        return [voice.name for voice in self.engine.getProperty('voices')]