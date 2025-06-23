from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QMovie

def setup_voice_animation(self):
    self.voice_label = QLabel(self)
    self.voice_movie = QMovie("mic_wave.gif")  # Use a waveform GIF
    self.voice_label.setMovie(self.voice_movie)
    self.voice_label.hide()

def start_listening_visual(self):
    self.voice_label.show()
    self.voice_movie.start()

def stop_listening_visual(self):
    self.voice_movie.stop()
    self.voice_label.hide()