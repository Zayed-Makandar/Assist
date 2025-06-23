from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QPushButton

class SettingsDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Settings")
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("AI Provider:"))
        self.provider_combo = QComboBox()
        self.provider_combo.addItems(["OpenAI", "Qwen", "Mock"])
        layout.addWidget(self.provider_combo)
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.accept)
        layout.addWidget(save_btn)