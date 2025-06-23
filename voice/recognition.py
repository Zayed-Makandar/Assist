import speech_recognition as sr
from PyQt6.QtCore import QObject, pyqtSignal
import threading

class VoiceRecognition(QObject):
    command_recognized = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.is_listening = False
        self._listen_thread = None
        self._lock = threading.Lock()

    def start(self):
        with self._lock:
            if self.is_listening:
                print("VoiceRecognition: Already listening, not starting again.")
                return            print("VoiceRecognition: Starting to listen.")
            self.is_listening = True
            self._listen_thread = threading.Thread(target=self._listen_loop, daemon=True)
            self._listen_thread.start()

    def stop(self):
        with self._lock:
            if not self.is_listening:
                print("VoiceRecognition: Not listening, nothing to stop.")
                return
            print("VoiceRecognition: Stopping listening.")
            self.is_listening = False

    def _listen_loop(self):
        recognizer = sr.Recognizer()
        mic = sr.Microphone()
        while self.is_listening:
            with mic as source:
                print("VoiceRecognition: Adjusting for ambient noise and listening for command...")
                recognizer.adjust_for_ambient_noise(source)
                try:
                    audio = recognizer.listen(source, timeout=5)
                    print("VoiceRecognition: Got audio, recognizing...")
                    command = recognizer.recognize_google(audio)
                    print(f"VoiceRecognition: Recognized command: {command}")
                    self.command_recognized.emit(command)
                except Exception as e:
                    print(f"VoiceRecognition: Listening error or timeout: {e}")
                    continue