from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QListWidget, QPushButton, QLabel, QApplication, QListWidgetItem, QFrame, QTextEdit, QFileDialog, QAction, QDialog, QComboBox, QSpinBox, QDialogButtonBox
)
from PyQt5.QtGui import QPixmap, QPainter, QBrush, QColor, QIcon, QMovie
from PyQt5.QtCore import Qt, QSize, QTimer, QPoint, pyqtSignal
import sys
import os
import speech_recognition as sr
from PyQt5.QtSvg import QSvgRenderer
from PyQt5.QtCore import QByteArray
from PyQt5.QtWidgets import QShortcut
from PyQt5.QtGui import QKeySequence

def get_windows_profile_pic():
    username = os.getlogin()
    account_pics_path = os.path.expandvars(r"C:\Users\%s\AppData\Roaming\Microsoft\Windows\AccountPictures" % username)
    if os.path.exists(account_pics_path):
        pics = [os.path.join(account_pics_path, f) for f in os.listdir(account_pics_path) if f.lower().endswith(('.jpg', '.png'))]
        if pics:
            pics.sort(key=os.path.getmtime, reverse=True)
            return pics[0]
    default_pic = r"C:\Users\crims\OneDrive\Pictures\_Z.jpg"
    if os.path.exists(default_pic):
        return default_pic
    return None

def get_round_pixmap(image_path, size=40):
    pixmap = QPixmap(image_path).scaled(size, size, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
    rounded = QPixmap(size, size)
    rounded.fill(Qt.transparent)
    painter = QPainter(rounded)
    painter.setRenderHint(QPainter.Antialiasing)
    brush = QBrush(pixmap)
    painter.setBrush(brush)
    painter.setPen(Qt.NoPen)
    painter.drawEllipse(0, 0, size, size)
    painter.end()
    return rounded

class ChatMessageWidget(QWidget):
    def __init__(self, text, profile_pic_path=None, parent=None):
        super().__init__(parent)
        self.text = text
        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        if profile_pic_path and os.path.exists(profile_pic_path):
            pic = get_round_pixmap(profile_pic_path, 40)
        else:
            pic = QPixmap(40, 40)
            pic.fill(Qt.transparent)
            painter = QPainter(pic)
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setBrush(QBrush(QColor("#888")))
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(0, 0, 40, 40)
            painter.end()
        pic_label = QLabel()
        pic_label.setPixmap(pic)
        pic_label.setFixedSize(40, 40)
        self.text_label = QLabel(text)  # <-- Assign to self.text_label
        self.text_label.setWordWrap(True)
        self.text_label.setStyleSheet("font-size: 14px; padding-left: 8px;")
        layout.addWidget(pic_label)
        layout.addWidget(self.text_label)
        layout.addStretch()
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

    def show_context_menu(self, pos):
        from PyQt5.QtWidgets import QMenu, QApplication
        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu { background-color: #fff; color: #222; border: 1px solid #bbb; }
            QMenu::item:selected { background-color: #2196F3; color: #fff; }
        """)
        copy_action = menu.addAction("Copy")
        delete_action = menu.addAction("Delete")
        action = menu.exec_(self.mapToGlobal(pos))
        if action == copy_action:
            QApplication.clipboard().setText(self.text_label.text())
        elif action == delete_action:
            # Remove this widget from the parent QListWidget
            parent = self.parentWidget()
            while parent and not isinstance(parent, QListWidget):
                parent = parent.parentWidget()
            if parent:
                for i in range(parent.count()):
                    if parent.itemWidget(parent.item(i)) == self:
                        parent.takeItem(i)
                        break

class AssistInputBox(QTextEdit):
    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self.main_window = main_window

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            if event.modifiers() == Qt.ShiftModifier:
                self.insertPlainText('\n')
            else:
                self.main_window.on_send_clicked()
        else:
            super().keyPressEvent(event)

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        layout = QVBoxLayout(self)
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Light", "Dark"])
        layout.addWidget(QLabel("Theme:"))
        layout.addWidget(self.theme_combo)
        self.font_size_spin = QSpinBox()
        self.font_size_spin.setRange(8, 32)
        self.font_size_spin.setValue(14)
        layout.addWidget(QLabel("Font Size:"))
        layout.addWidget(self.font_size_spin)
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def get_settings(self):
        return {
            "theme": self.theme_combo.currentText(),
            "font_size": self.font_size_spin.value()
        }

class AssistAvatarWidget(QWidget):
    def __init__(self, avatar_path=None, size=40, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self.avatar_label = QLabel(self)
        # Custom half-blue, half-black circle
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        # Draw left half blue
        painter.setBrush(QBrush(QColor("#2196F3")))  # Blue
        painter.setPen(Qt.NoPen)
        painter.drawPie(0, 0, size, size, 90 * 16, 180 * 16)
        # Draw right half black
        painter.setBrush(QBrush(QColor("#000000")))  # Black
        painter.drawPie(0, 0, size, size, 270 * 16, 180 * 16)
        painter.end()
        self.avatar_label.setPixmap(pixmap)
        self.avatar_label.setFixedSize(size, size)
        layout.addWidget(self.avatar_label)
        layout.addStretch()

class TypingIndicatorWidget(QWidget):
    def __init__(self, avatar_path=None, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)
        self.avatar = AssistAvatarWidget(avatar_path=avatar_path, size=32)
        layout.addWidget(self.avatar)
        self.spinner_label = QLabel(self)
        self.spinner = QMovie("spinner.gif")
        self.spinner.setScaledSize(QSize(24, 24))
        self.spinner_label.setMovie(self.spinner)
        self.spinner.start()
        layout.addWidget(self.spinner_label)
        self.label = QLabel("Assist is typing", self)
        self.label.setStyleSheet("color: #000000; font-size: 15px;")  # Black text
        layout.addWidget(self.label)
        layout.addStretch()
        self.setStyleSheet("background: #f0f0f0; border-radius: 12px;")
        self.setFixedHeight(36)
        self.dots = ""
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate)
        self.timer.start(500)

    def animate(self):
        self.dots = "." * ((len(self.dots) % 3) + 1)
        self.label.setText(f"Assist is typing{self.dots}")

class HistoryDialog(QDialog):
    def __init__(self, history_items, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Chat History")
        layout = QVBoxLayout(self)
        self.list_widget = QListWidget()  # <-- Initialize before using
        for item in history_items:
            self.list_widget.addItem(item)
        layout.addWidget(self.list_widget)
        close_btn = QDialogButtonBox(QDialogButtonBox.Close)
        close_btn.rejected.connect(self.reject)
        layout.addWidget(close_btn)

class AssistMainWindow(QMainWindow):
    command_sent = pyqtSignal(str)  # Add this signal

    def __init__(self):
        super().__init__()
        self.assist_logo_path = "assist_logo.png"
        self.setWindowTitle("Assist")
        self.setWindowIcon(QIcon(self.assist_logo_path))
        menubar = self.menuBar()
        self.dropdown_menu = menubar.addMenu("Menu")
        about_menu = menubar.addMenu("About")
        about_action = QAction("Team Info", self)
        about_action.triggered.connect(self.show_about)
        about_menu.addAction(about_action)

        # Add this block to display a larger logo at the top
        logo_label = QLabel()
        logo_pixmap = QPixmap(self.assist_logo_path)
        logo_label.setPixmap(logo_pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))  # Adjust size as needed
        logo_label.setAlignment(Qt.AlignCenter)
        # Central chat area
        self.chat_area = QListWidget()
        self.chat_area.setFrameShape(QFrame.NoFrame)
        self.chat_area.setStyleSheet("background: white;")
        self.chat_area.setSpacing(8)
        self.user_pic_path = get_windows_profile_pic()
        menubar = self.menuBar()
        #self.dropdown_menu = menubar.addMenu("Menu")
        history_action = QAction("History", self)
        history_action.triggered.connect(self.show_history)
        profile_action = QAction("Profile", self)
        profile_action.triggered.connect(self.choose_profile_picture)
        settings_action = QAction("Settings", self)
        settings_action.triggered.connect(self.open_settings)
        self.dropdown_menu.addAction(history_action)
        self.dropdown_menu.addAction(profile_action)
        self.dropdown_menu.addAction(settings_action)
        self.input_box = AssistInputBox(self)
        self.input_box.setFixedHeight(40)
        self.send_btn = QPushButton("Send")
        self.mic_btn = QPushButton()
        mic_svg = '''
        <svg width="24" height="24" viewBox="0 0 18 18" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M11.165 4.41699C11.165 3.22048 10.1955 2.25018 8.99902 2.25C7.80241 2.25 6.83203 3.22038 6.83203 4.41699V8.16699C6.83221 9.36346 7.80252 10.333 8.99902 10.333C10.1954 10.3328 11.1649 9.36335 11.165 8.16699V4.41699ZM12.665 8.16699C12.6649 10.1918 11.0238 11.8328 8.99902 11.833C6.97409 11.833 5.33221 10.1919 5.33203 8.16699V4.41699C5.33203 2.39195 6.97398 0.75 8.99902 0.75C11.0239 0.750176 12.665 2.39206 12.665 4.41699V8.16699Z" fill="black"/>
        <path d="M6.25 13.25C6.25 13.6642 6.58579 14 7 14H11C11.4142 14 11.75 13.6642 11.75 13.25C11.75 12.8358 11.4142 12.5 11 12.5H7C6.58579 12.5 6.25 12.8358 6.25 13.25Z" fill="black"/>
        </svg>
        '''
        svg_bytes = QByteArray(mic_svg.encode('utf-8'))
        renderer = QSvgRenderer(svg_bytes)
        pixmap = QPixmap(32, 32)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        renderer.render(painter)
        painter.end()
        self.mic_btn.setIcon(QIcon(pixmap))
        self.mic_btn.setIconSize(QSize(24, 24))
        self.mic_btn.setFixedSize(40, 40)
        self.mic_btn.setCheckable(True)
        self.mic_btn.setStyleSheet("border: none; background: transparent;")
        self.mic_btn.clicked.connect(self.on_mic_clicked)
        self.mic_btn.installEventFilter(self)
        self.dictate_label = QLabel("Voice input", self)
        self.dictate_label.setStyleSheet("background: #222; color: white; border-radius: 6px; padding: 2px 8px; font-weight: bold;")
        self.dictate_label.setVisible(False)
        self.dictate_label.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.dictate_label.adjustSize()
        self.processing_label = QLabel()
        self.processing_label.setVisible(False)
        self.spinner = QMovie("spinner.gif")
        self.spinner.setScaledSize(QSize(24, 24))
        self.processing_label.setMovie(self.spinner)
        self.processing_label.setFixedSize(24, 24)
        self.processing_label.setStyleSheet("padding-left: 8px;")
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.input_box)
        input_layout.addWidget(self.mic_btn)
        input_layout.addWidget(self.send_btn)
        processing_layout = QHBoxLayout()
        processing_layout.addWidget(self.processing_label)
        processing_layout.addStretch()
        main_layout = QVBoxLayout()
        main_layout.addWidget(logo_label)  # Add logo at the top
        main_layout.addWidget(self.chat_area)
        main_layout.addLayout(processing_layout)
        main_layout.addLayout(input_layout)
        central_widget = QWidget()
        layout = QHBoxLayout(central_widget)
        layout.addLayout(main_layout)
        self.setCentralWidget(central_widget)
        self.status = self.statusBar()
        self.status.showMessage("Ready")
        self.send_btn.clicked.connect(self.on_send_clicked)
        self.theme = "Light"
        self.font_size = 14

    def on_send_clicked(self):
        text = self.input_box.toPlainText().strip()
        if text:
            item = QListWidgetItem()
            widget = ChatMessageWidget(text, self.user_pic_path)
            item.setSizeHint(widget.sizeHint())
            self.chat_area.addItem(item)
            self.chat_area.setItemWidget(item, widget)
            self.chat_area.scrollToBottom()
            self.input_box.clear()
            self.command_sent.emit(text)
    
    def show_about(self):
        about_dialog = AboutDialog(self)
        about_dialog.exec_()

    def choose_profile_picture(self):
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter("Images (*.png *.jpg *.jpeg *.bmp)")
        if file_dialog.exec_():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                self.user_pic_path = selected_files[0]
                self.show_info("Profile picture updated!")

    def open_settings(self):
        dlg = SettingsDialog(self)
        dlg.theme_combo.setCurrentText(self.theme)
        dlg.font_size_spin.setValue(self.font_size)
        if dlg.exec_():
            settings = dlg.get_settings()
            self.theme = settings["theme"]
            self.font_size = settings["font_size"]
            self.apply_personalization()

    def apply_personalization(self):
        if self.theme == "Dark":
            self.setStyleSheet("background: #222; color: #eee;")
            self.chat_area.setStyleSheet("background: #333; color: #eee;")
        else:
            self.setStyleSheet("")
            self.chat_area.setStyleSheet("background: white; color: black;")
        self.input_box.setStyleSheet(f"font-size: {self.font_size}px;")

    def on_mic_clicked(self):
        if self.mic_btn.isChecked():
            self.mic_btn.setStyleSheet("background: #4caf50;")
            self.status.showMessage("Listening for voice input...")
            QApplication.processEvents()
            recognizer = sr.Recognizer()
            with sr.Microphone() as source:
                try:
                    audio = recognizer.listen(source, timeout=5)
                    text = recognizer.recognize_google(audio)
                    self.input_box.setPlainText(text)
                    self.status.showMessage("Voice input received.")
                except sr.WaitTimeoutError:
                    self.status.showMessage("Listening timed out. Try again.")
                except sr.UnknownValueError:
                    self.status.showMessage("Could not understand audio.")
                except sr.RequestError:
                    self.status.showMessage("Speech recognition service error.")
                finally:
                    self.mic_btn.setChecked(False)
                    self.mic_btn.setStyleSheet("")
        else:
            self.mic_btn.setStyleSheet("")
            self.status.showMessage("Ready")

    def eventFilter(self, obj, event):
        if obj == self.mic_btn:
            if event.type() == event.Enter:
                self.dictate_label.setText("Voice input")
                self.dictate_label.adjustSize()
                btn_pos = self.mic_btn.mapToGlobal(QPoint(0, 0))
                local_pos = self.mapFromGlobal(btn_pos)
                # Calculate available space below and above the mic button
                window_height = self.height()
                mic_bottom = local_pos.y() + self.mic_btn.height()
                mic_top = local_pos.y()
                label_height = self.dictate_label.height()
                # Default: show below
                y = mic_bottom + 4
                # If not enough space below, show above
                if mic_bottom + label_height + 10 > window_height:
                    y = mic_top - label_height - 4
                self.dictate_label.move(
                    local_pos.x() + self.mic_btn.width() // 2 - self.dictate_label.width() // 2,
                    y
                )
                self.dictate_label.setVisible(True)
            elif event.type() == event.Leave:
                self.dictate_label.setVisible(False)
        return super().eventFilter(obj, event)

    def show_error(self, message):
        try:
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.critical(self, "Error", message)
            self.status.showMessage("Error: " + message, 5000)
        except Exception:
            self.status.showMessage("Error: " + message, 5000)

    def show_info(self, message):
        if message == "Command sent!":
            self.typing_item = QListWidgetItem()
            self.typing_widget = TypingIndicatorWidget(avatar_path=self.assist_logo_path)
            self.typing_item.setSizeHint(self.typing_widget.sizeHint())
            self.chat_area.addItem(self.typing_item)
            self.chat_area.setItemWidget(self.typing_item, self.typing_widget)
            # Ensure the typing indicator is removed after a delay
            QTimer.singleShot(2000, self.hide_processing)
        else:
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.information(self, "Info", message)
            self.status.showMessage(message, 3000)

    def hide_processing(self):
        if hasattr(self, "typing_item"):
            row = self.chat_area.row(self.typing_item)
            if row != -1:
                self.chat_area.takeItem(row)
            del self.typing_item
            del self.typing_widget

    def introduce_assist(self):
        slogan = "Assist - Where Help Meets Intelligence"
        item = QListWidgetItem()
        widget = ChatMessageWidget(slogan, self.assist_logo_path)
        item.setSizeHint(widget.sizeHint())
        self.chat_area.addItem(item)
        self.chat_area.setItemWidget(item, widget)
        self.chat_area.scrollToBottom()

    def add_ai_message(self, text):
        item = QListWidgetItem()
        widget = ChatMessageWidget(text, self.assist_logo_path)
        item.setSizeHint(widget.sizeHint())
        self.chat_area.addItem(item)
        self.chat_area.setItemWidget(item, widget)
        self.chat_area.scrollToBottom()
        self.input_box.clear()
        self.show_info("Command sent!")
        QTimer.singleShot(2000, self.hide_processing)  # This should remove the typing indicator
        # self.command_sent.emit(text)  # <-- REMOVE or COMMENT OUT THIS LINE
        self.chat_visible = True
        self.shortcut = QShortcut(QKeySequence("Alt+C"), self)
        self.shortcut.activated.connect(self.toggle_chat_visibility)

    def toggle_chat_visibility(self):
        if self.chat_visible:
            self.hide()
        else:
            self.show()
        self.chat_visible = not self.chat_visible

    def show_history(self):
        # For demonstration, collect all chat messages from the chat_area
        history = []
        for i in range(self.chat_area.count()):
            widget = self.chat_area.itemWidget(self.chat_area.item(i))
            if isinstance(widget, ChatMessageWidget):
                # Assuming the text label is the second widget in the layout
                text_label = widget.layout().itemAt(1).widget()
                if isinstance(text_label, QLabel):
                    history.append(text_label.text())
        dlg = HistoryDialog(history, self)
        dlg.exec_()

    def exit_voice_input_mode(self):
        # This can be expanded to actually stop voice input if needed
        self.mic_btn.setChecked(False)
        self.mic_btn.setStyleSheet("")
        self.status.showMessage("Ready")
        self.send_btn.clicked.connect(self.on_send_clicked)
        self.theme = "Light"
        self.font_size = 14
        self.resize(500, 600)  # Set your preferred default size
        self.move(800, 100)    # Set your preferred default position (optional)

    def closeEvent(self, event):
        print("[DEBUG] closeEvent triggered")
        try:
            print("[DEBUG] Attempting to stop backend components...")
            self.backend.voice.stop()
            print("[DEBUG] Voice stopped")
            self.backend.wakeword.stop()
            print("[DEBUG] Wakeword stopped")
            self.backend.tts.stop()
            print("[DEBUG] TTS stopped")
            print("[DEBUG] Unhooking all keyboard hotkeys...")
            keyboard.unhook_all_hotkeys()
            keyboard.unhook_all()
            print("[DEBUG] Keyboard hooks unhooked")
        except Exception as e:
            print(f"Cleanup error: {e}")
        print("[DEBUG] Calling QApplication.quit()")
        QApplication.quit()
        print("[DEBUG] QApplication.quit() called, window should close.")
        event.accept()

class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("About Assist")
        self.setFixedSize(300, 200)
        
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        
        # Team name with styling
        team_label = QLabel("Team ZAY")
        team_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #2196F3;")
        team_label.setAlignment(Qt.AlignCenter)
        
        # Team members
        members_label = QLabel("(Zaid, AI, Yasin)")
        members_label.setStyleSheet("font-size: 14px;")
        members_label.setAlignment(Qt.AlignCenter)
        
        # Project title
        project_label = QLabel("Assist - Where Help Meets Intelligence")
        project_label.setStyleSheet("font-size: 14px; font-style: italic; margin-top: 20px;")
        project_label.setAlignment(Qt.AlignCenter)
        
        # Add widgets to layout
        layout.addWidget(team_label)
        layout.addWidget(members_label)
        layout.addWidget(project_label)
        layout.addStretch()