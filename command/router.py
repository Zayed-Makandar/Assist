from PyQt6.QtCore import QObject, pyqtSignal

class CommandRouter(QObject):
    system_command = pyqtSignal(str)
    execution_started = pyqtSignal(str)
    execution_completed = pyqtSignal(str)

    def __init__(self):
        super().__init__()

    def route_command(self, command):
        self.execution_started.emit(command)
        # For now, just echo the command as a system command
        self.system_command.emit(command)
        self.execution_completed.emit(f"Executed: {command}")