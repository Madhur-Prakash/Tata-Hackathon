import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl

def main():
    app = QApplication(sys.argv)
    window = QWidget()
    layout = QVBoxLayout()
    view = QWebEngineView()

    # Load the FastAPI backend URL serving your map
    url = QUrl("http://127.0.0.1:8000/")
    view.load(url)

    layout.addWidget(view)
    window.setLayout(layout)
    window.setWindowTitle("Map Viewer via FastAPI")
    window.resize(1200, 800)
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
