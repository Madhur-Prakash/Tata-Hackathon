import sys
import os
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt6.QtWebEngineWidgets import QWebEngineView


base_dir = os.path.dirname(os.path.abspath(__file__))  # this gets frontend/
map_path = os.path.join(base_dir, "map.html")
with open(map_path, 'r', encoding='utf-8') as file:
    map_html = file.read()
app = QApplication(sys.argv)
window = QWidget()
layout = QVBoxLayout()
view = QWebEngineView()
view.setHtml(map_html)
layout.addWidget(view)
window.setLayout(layout)
window.show()
sys.exit(app.exec())