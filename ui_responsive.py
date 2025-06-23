from PyQt5.QtWidgets import QSizePolicy

def make_responsive(self):
    self.chat_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    self.sidebar.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)