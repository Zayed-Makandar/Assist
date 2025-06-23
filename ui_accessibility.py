def set_accessible_fonts(self):
    font = self.font()
    font.setPointSize(12)
    self.setFont(font)
    self.input_box.setToolTip("Type your command here")
    self.send_btn.setToolTip("Send command")