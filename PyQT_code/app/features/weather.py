import requests
from PyQt6.QtWidgets import QFrame, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt, QObject, QThread, pyqtSignal, pyqtSlot
from .. import config

def weather_code_to_info(code):
    if code == 0: return "Clear sky", "☀️"
    if code in [1, 2, 3]: return "Mainly clear", "🌤️"
    if code in [45, 48]: return "Fog", "🌫️"
    if code in [51, 53, 55]: return "Drizzle", "🌦️"
    if code in [61, 63, 65]: return "Rain", "🌧️"
    if code in [80, 81, 82]: return "Rain showers", "🌧️"
    if code in [71, 73, 75]: return "Snowfall", "❄️"
    if code == 95: return "Thunderstorm", "⛈️"
    return "Unknown", "❓"

class WeatherWorker(QObject):
    data_ready = pyqtSignal(dict)
    @pyqtSlot()
    def fetch_weather(self):
        try:
            lat, lon = 28.4595, 77.0266
            url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            self.data_ready.emit(response.json())
        except requests.exceptions.RequestException as e:
            self.data_ready.emit({"error": str(e)})

class WeatherWidget(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("WeatherWidgetFrame")
        self.setStyleSheet(f"""
            QFrame#WeatherWidgetFrame {{
                background-color: {config.WIDGET_BACKGROUND_COLOR};
                border-radius: 10px;
            }}
            QLabel {{ background-color: transparent; color: white; }}
        """)
        self.info_label = QLabel("Weather data will load...", alignment=Qt.AlignmentFlag.AlignCenter)
        layout = QVBoxLayout(self); layout.addWidget(self.info_label)
        self._setup_thread()

    def _setup_thread(self):
        self.thread = QThread(); self.worker = WeatherWorker()
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.fetch_weather)
        self.worker.data_ready.connect(self.update_weather_display)
        self.worker.data_ready.connect(self.thread.quit)

    def start_updates(self):
        if not self.thread.isRunning(): self.info_label.setText("Fetching weather..."); self.thread.start()
    def stop_updates(self):
        if self.thread.isRunning(): self.thread.quit(); self.thread.wait(2000)

    def update_weather_display(self, data):
        if "error" in data: self.info_label.setText(f"Error:<br>{data['error']}"); return
        try:
            current = data.get("current_weather", {}); temp = current.get("temperature", "N/A"); code = current.get("weathercode", -1)
            description, emoji = weather_code_to_info(code)
            html_text = f"""<div style='text-align:center;'><span style='font-size: 48px;'>{emoji}</span><br/><span style='font-size: 32px; font-weight: bold;'>{temp}°C</span><br/><span style='font-size: 18px;'>{description}</span></div>"""
            self.info_label.setText(html_text)
        except (AttributeError, TypeError): self.info_label.setText("Error:<br>Could not parse data.")