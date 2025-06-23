from PyQt5.QtWidgets import QCompleter

def update_history(self, command):
    self.sidebar.addItem(command)

def setup_completer(self, commands):
    completer = QCompleter(commands)
    self.input_box.setCompleter(completer)