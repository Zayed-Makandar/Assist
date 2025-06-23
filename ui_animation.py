from PyQt5.QtCore import QPropertyAnimation

def animate_popup(self, widget):
    anim = QPropertyAnimation(widget, b"windowOpacity")
    anim.setDuration(500)
    anim.setStartValue(0)
    anim.setEndValue(1)
    anim.start()