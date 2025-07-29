from PyQt6.QtWidgets import QWidget, QPushButton, QHBoxLayout

class ToggleButton(QWidget):
    def __init__(self, on_text="On", off_text="Off", on_color="#00cc99", off_color="#2A2A2A", parent=None):
        super().__init__(parent)
        self.on_text = on_text
        self.off_text = off_text
        self.on_color = on_color
        self.off_color = off_color

        self.button = QPushButton(self.off_text)
        self.button.setCheckable(True)
        self.button.setStyleSheet(self._button_style(False))
        self.button.toggled.connect(self._toggle_state)

        layout = QHBoxLayout(self)
        layout.addWidget(self.button)
        layout.setContentsMargins(0, 0, 0, 0)

    def _toggle_state(self, checked):
        self.button.setText(self.on_text if checked else self.off_text)
        self.button.setStyleSheet(self._button_style(checked))

    def _button_style(self, checked):
        color = self.on_color if checked else self.off_color
        return f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border-radius: 15px;
                padding: 5px 15px;
                font-weight: bold;
            }}
        """