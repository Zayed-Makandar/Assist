import pvporcupine
import pyaudio
import struct
import threading
from PyQt6.QtCore import QObject, pyqtSignal

class WakeWordListener(QObject):
    wake_word_detected = pyqtSignal()

    def __init__(self, keyword_path=None, access_key="ede+N895C+y2ceCslqlYXS31V3PUYiwMIVDmSIh2RwiRR0mhmm8zOw=="):
        super().__init__()
        self._running = False
        self._thread = None

        if keyword_path:
            self.porcupine = pvporcupine.create(
                access_key=access_key,
                keyword_paths=[keyword_path]
            )
        else:
            self.porcupine = pvporcupine.create(
                access_key=access_key,
                keywords=["porcupine"]
            )

        self.pa = pyaudio.PyAudio()
        self.audio_stream = self.pa.open(
            rate=self.porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=self.porcupine.frame_length
        )

    def start(self):
        self._running = True
        self._thread = threading.Thread(target=self._listen, daemon=True)
        self._thread.start()

    def stop(self):
        self._running = False
        if self._thread:
            self._thread.join()
        self.audio_stream.stop_stream()
        self.audio_stream.close()
        self.pa.terminate()
        self.porcupine.delete()

    def _listen(self):
        while self._running:
            pcm = self.audio_stream.read(self.porcupine.frame_length, exception_on_overflow=False)
            pcm = struct.unpack_from("h" * self.porcupine.frame_length, pcm)
            result = self.porcupine.process(pcm)
            if result >= 0:
                self.wake_word_detected.emit()