# app/splash_screen.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtGui import QMovie
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QSize

from .config import get_asset_path, SPLASH_SCREEN_TIMEOUT

class SplashScreen(QWidget):
    # Signal to indicate when the splash screen is done
    finished = pyqtSignal()

    def __init__(self):
        super().__init__()
        
        # Configure the window to be frameless and transparent
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(600, 500)

        layout = QVBoxLayout(self)
        
        # Display the loading animation
        self.loading_label = QLabel()
        try:
            gif_path = get_asset_path("loader.gif")
            movie = QMovie(gif_path)
            movie.setScaledSize(QSize(400, 300)) # Ensure GIF fits
            self.loading_label.setMovie(movie)
            movie.start()
        except Exception:
            self.loading_label.setText("Loading...")
            self.loading_label.setStyleSheet("color: white; font-size: 24px;")

        layout.addWidget(self.loading_label, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Use the timeout from the config file
        # QTimer.singleShot(SPLASH_SCREEN_TIMEOUT, self.finish_splash)
        QTimer.singleShot(1500, self.finish_splash)

    def finish_splash(self):
        """Closes the splash screen and signals that it's done."""
        self.finished.emit()
        self.close()