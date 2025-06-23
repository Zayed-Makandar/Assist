"""
Side panel component for displaying additional information
"""
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QScrollArea
from PyQt6.QtCore import Qt, pyqtSlot
from PyQt6.QtGui import QFont, QColor, QPalette
import logging
import sys
import os

# Add parent directory to path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

logger = logging.getLogger(__name__)

class SidePanel(QWidget):
    """Side panel widget for displaying additional information"""
    
    def __init__(self):
        """Initialize the side panel widget"""
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
        self.resize(config.SIDE_PANEL_WIDTH, 600)
        
        # Position the window on the right side of the screen
        self._position_on_screen()
        
        # Initialize UI components
        self._init_ui()
        
        logger.info("Side panel initialized")
    
    def _init_ui(self):
        """Initialize UI components"""
        # Create layout
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Create title label
        self.title_label = QLabel("Assist Information")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        
        # Create scroll area for content
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        
        # Create content widget
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        
        # Create content label
        self.content_label = QLabel("No information available")
        self.content_label.setWordWrap(True)
        self.content_label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.content_label.setFont(QFont("Arial", 11))
        
        # Add content label to content layout
        self.content_layout.addWidget(self.content_label)
        
        # Set content widget as scroll area widget
        self.scroll_area.setWidget(self.content_widget)
        
        # Apply theme
        self._apply_theme()
        
        # Add components to layout
        layout.addWidget(self.title_label)
        layout.addWidget(self.scroll_area)
        
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
        
        # Apply to content widget
        self.content_widget.setPalette(palette)
        self.content_widget.setAutoFillBackground(True)
    
    def _position_on_screen(self):
        """Position the window on the right side of the screen"""
        screen_geometry = self.screen().geometry()
        x = screen_geometry.width() - self.width() - 20
        y = (screen_geometry.height() - self.height()) // 2
        self.move(x, y)
    
    @pyqtSlot(str)
    def show_information(self, information):
        """Show information in the side panel"""
        logger.debug(f"Showing information: {information}")
        self.content_label.setText(information)
        self.show()
    
    @pyqtSlot(str)
    def append_information(self, information):
        """Append information to the side panel"""
        current_text = self.content_label.text()
        if current_text == "No information available":
            current_text = ""
        new_text = f"{current_text}\n\n{information}" if current_text else information
        self.content_label.setText(new_text)
        self.show()
    
    def keyPressEvent(self, event):
        from PyQt6.QtCore import Qt
        if event.key() == Qt.Key.Key_Escape:
            self.close()