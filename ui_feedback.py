from PyQt5.QtWidgets import QMessageBox, QProgressBar

def show_info(self, message):
    QMessageBox.information(self, "Info", message)

def show_error(self, message):
    QMessageBox.critical(self, "Error", message)

def show_loading(self):
    self.progress = QProgressBar(self)
    self.progress.setRange(0, 0)  # Indeterminate
    self.statusBar().addWidget(self.progress)

def hide_loading(self):
    if hasattr(self, 'progress'):
        self.statusBar().removeWidget(self.progress)
        del self.progress