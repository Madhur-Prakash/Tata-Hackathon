import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl

class MapWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OSM in PyQt")
        self.setGeometry(100, 100, 1200, 800)

        self.browser = QWebEngineView()

        # Get the absolute path to `map.html` within the 'frontend' folder
        base_dir = os.path.dirname(os.path.abspath(__file__))  # this gets frontend/
        map_path = os.path.join(base_dir, "map.html")

        # Load the local HTML file
        self.browser.load(QUrl.fromLocalFile(map_path))
        self.setCentralWidget(self.browser)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MapWindow()
    window.show()
    sys.exit(app.exec())
