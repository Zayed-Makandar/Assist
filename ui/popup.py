"""
Center popup component for displaying commands and responses
"""
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt, pyqtSlot
from PyQt6.QtGui import QFont, QColor, QPalette
import logging
import sys
import os

# Add parent directory to path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

logger = logging.getLogger(__name__)

class CenterPopup(QWidget):
    """Center popup widget for displaying commands and responses"""
    
    def __init__(self):
        """Initialize the popup widget"""
        super().__init__()
        
        # Set window flags to create a frameless, always-on-top window
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | 
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        
        # Set window opacity
        self.setWindowOpacity(config.POPUP_OPACITY)
        
        # Set window size
        self.resize(config.POPUP_WIDTH, config.POPUP_HEIGHT)
        
        # Center the window on the screen
        self._center_on_screen()
        
        # Initialize UI components
        self._init_ui()
        
        logger.info("Center popup initialized")
    
    def _init_ui(self):
        """Initialize UI components"""
        # Create layout
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Create message label
        self.message_label = QLabel("Assist")
        self.message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.message_label.setFont(QFont("Arial", 16))
        
        # Apply theme
        self._apply_theme()
        
        # Add components to layout
        layout.addWidget(self.message_label)
        
        # Set layout
        self.setLayout(layout)
    
    def _apply_theme(self):
        """Apply theme to UI components"""
        palette = QPalette()
        
        if config.UI_THEME == "dark":
            # Dark theme
            background_color = QColor(40, 40, 40)
            text_color = QColor(240, 240, 240)
        else:
            # Light theme
            background_color = QColor(240, 240, 240)
            text_color = QColor(40, 40, 40)
        
        # Set background color
        palette.setColor(QPalette.ColorRole.Window, background_color)
        palette.setColor(QPalette.ColorRole.WindowText, text_color)
        
        # Apply palette
        self.setPalette(palette)
        self.setAutoFillBackground(True)
    
    def _center_on_screen(self):
        """Center the window on the screen"""
        screen_geometry = self.screen().geometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.move(x, y)
    
    @pyqtSlot(str)
    def show_message(self, message):
        """Show a message in the popup"""
        logger.debug(f"Showing message: {message}")
        self.message_label.setText(message)
        self.show()
    
    @pyqtSlot(str)
    def show_command(self, command):
        """Show a recognized command"""
        self.show_message(f"Command: {command}")
    
    @pyqtSlot(str)
    def show_execution(self, message):
        """Show execution status"""
        self.show_message(f"Executing: {message}")
    
    @pyqtSlot(str)
    def show_result(self, result):
        """Show execution result"""
        self.show_message(f"Result: {result}")
    
    def keyPressEvent(self, event):
        from PyQt6.QtCore import Qt
        if event.key() == Qt.Key.Key_Escape:
            self.close()