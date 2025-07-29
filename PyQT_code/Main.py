import sys
from PyQt6.QtWidgets import QApplication
from app.splash_screen import SplashScreen
from app.main_window import MainWindow

class AppRunner:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.main_window = None
        self.splash = SplashScreen()
        self.splash.finished.connect(self.show_main_window)

    def run(self):
        screen_geometry = self.app.primaryScreen().geometry()
        self.splash.move(screen_geometry.center() - self.splash.rect().center())
        self.splash.show()
        return self.app.exec()

    def show_main_window(self):
        self.main_window = MainWindow()
        self.main_window.show()

if __name__ == "__main__":
    runner = AppRunner()
    sys.exit(runner.run())
    