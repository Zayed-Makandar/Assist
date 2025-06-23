"""
Visual feedback system for displaying operation status
"""
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, pyqtSlot
from PyQt6.QtGui import QFont, QColor, QPalette
import logging
import sys
import os

# Add parent directory to path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

logger = logging.getLogger(__name__)

class VisualFeedback(QWidget):
    """Visual feedback widget for displaying operation status"""
    
    # Signals
    feedback_shown = pyqtSignal()
    feedback_hidden = pyqtSignal()
    
    def __init__(self):
        """Initialize the visual feedback widget"""
        super().__init__()
        
        # Set window flags to create a frameless, always-on-top window
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | 
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        
        # Set window opacity
        self.setWindowOpacity(0.8)
        
        # Set window size
        self.resize(300, 100)
        
        # Position the window in the bottom right corner
        self._position_on_screen()
        
        # Initialize UI components
        self._init_ui()
        
        # Create timer for auto-hiding
        self.hide_timer = QTimer(self)
        self.hide_timer.timeout.connect(self.hide)
        
        logger.info("Visual feedback initialized")
    
    def _init_ui(self):
        """Initialize UI components"""
        # Create layout
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Create status label
        self.status_label = QLabel("Ready")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setFont(QFont("Arial", 12))
        
        # Apply theme
        self._apply_theme()
        
        # Add components to layout
        layout.addWidget(self.status_label)
        
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
    
    def _position_on_screen(self):
        """Position the window in the bottom right corner"""
        screen_geometry = self.screen().geometry()
        x = screen_geometry.width() - self.width() - 20
        y = screen_geometry.height() - self.height() - 40
        self.move(x, y)
    
    @pyqtSlot(str, int)
    def show_status(self, status, duration=3000):
        """Show status for a specified duration"""
        logger.debug(f"Showing status: {status} for {duration}ms")
        self.status_label.setText(status)
        self.show()
        self.feedback_shown.emit()
        
        # Reset and start the hide timer
        self.hide_timer.stop()
        self.hide_timer.start(duration)
    
    @pyqtSlot(str)
    def show_success(self, message):
        """Show success message"""
        self._set_status_color(QColor(0, 180, 0))  # Green
        self.show_status(f"✓ {message}")
    
    @pyqtSlot(str)
    def show_error(self, message):
        """Show error message"""
        self._set_status_color(QColor(180, 0, 0))  # Red
        self.show_status(f"✗ {message}")
    
    @pyqtSlot(str)
    def show_info(self, message):
        """Show info message"""
        self._set_status_color(QColor(0, 120, 180))  # Blue
        self.show_status(f"ℹ {message}")
    
    @pyqtSlot(str)
    def show_warning(self, message):
        """Show warning message"""
        self._set_status_color(QColor(180, 120, 0))  # Orange
        self.show_status(f"⚠ {message}")
    
    def _set_status_color(self, color):
        """Set the status label text color"""
        palette = self.status_label.palette()
        palette.setColor(QPalette.ColorRole.WindowText, color)
        self.status_label.setPalette(palette)
    
    def hide(self):
        """Hide the feedback widget"""
        super().hide()
        self.feedback_hidden.emit()