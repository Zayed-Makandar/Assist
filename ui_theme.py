def set_dark_theme(self):
    self.setStyleSheet("""
        QMainWindow { background: #232629; color: #f0f0f0; }
        QTextEdit, QListWidget { background: #2e3136; color: #f0f0f0; }
        QPushButton { background: #3a3f44; color: #f0f0f0; }
    """)