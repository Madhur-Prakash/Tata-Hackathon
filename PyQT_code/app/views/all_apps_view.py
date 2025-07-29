from PyQt6.QtWidgets import QWidget, QPushButton, QGridLayout
from PyQt6.QtCore import pyqtSignal, QSize
from PyQt6.QtGui import QIcon

from .. import config

class AllAppsView(QWidget):
    view_change_requested = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QGridLayout(self)
        youtube_button = QPushButton("YouTube")
        yt_music_button = QPushButton("YouTube Music")
        youtube_button.setIcon(QIcon(config.get_asset_path("YouTube")))  
        yt_music_button.setIcon(QIcon(config.get_asset_path("YouTube_Music")))  
        youtube_button.setIconSize(QSize(44, 44))
        yt_music_button.setIconSize(QSize(44, 44))
        
        button_style = """
            QPushButton {
                background-color: #36363F; color: white; border-radius: 10px;
                padding: 20px; font-size: 18px; font-weight: bold;
            }
            QPushButton:pressed { background-color: #4a4a52; }
        """
        youtube_button.setStyleSheet(button_style)
        yt_music_button.setStyleSheet(button_style)
        
        youtube_button.clicked.connect(lambda: self.view_change_requested.emit("youtube"))
        yt_music_button.clicked.connect(lambda: self.view_change_requested.emit("yt_music"))
        
        layout.addWidget(youtube_button, 0, 0)
        layout.addWidget(yt_music_button, 0, 1)