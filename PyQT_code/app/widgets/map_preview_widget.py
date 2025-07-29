from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import Qt, QTimer, QUrl
from .. import config

class MapPreviewWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(200, 150)
        self.setStyleSheet(
            f"background-color: {config.WIDGET_BACKGROUND_COLOR};"
            "border-radius: 10px;"
        )
        
        # Create layout
        layout = QVBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        self.setLayout(layout)
        
        # Create web view for displaying HTML map
        self.web_view = QWebEngineView()
        self.web_view.setStyleSheet("border-radius: 5px;")
        
        # Load the map URL
        self.map_url = "http://127.0.0.1:8000"
        self.web_view.load(QUrl(self.map_url))
        
        # Handle loading states
        self.web_view.loadStarted.connect(self.on_load_started)
        self.web_view.loadFinished.connect(self.on_load_finished)
        
        # Add web view to layout
        layout.addWidget(self.web_view)
        
        # Timer for periodic map updates (optional)
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.refresh_map)
        
        # Create loading label (initially hidden)
        self.loading_label = QLabel("Loading map...")
        self.loading_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.loading_label.setStyleSheet(
            "border-radius: 5px;"
            "color: #888888;"
            "background-color: rgba(0, 0, 0, 0.7);"
            "padding: 10px;"
        )
        self.loading_label.hide()
        layout.addWidget(self.loading_label)
        
    def on_load_started(self):
        """Handle when map starts loading"""
        self.loading_label.setText("Loading map...")
        self.loading_label.show()
        self.web_view.hide()
        
    def on_load_finished(self, success):
        """Handle when map finishes loading"""
        self.loading_label.hide()
        self.web_view.show()
        
        if not success:
            self.loading_label.setText("Map unavailable\nFailed to load from server")
            self.loading_label.show()
            self.web_view.hide()
    
    def refresh_map(self):
        """Refresh the map by reloading the URL"""
        self.web_view.reload()
        
    def set_map_url(self, url):
        """Change the map URL"""
        self.map_url = url
        self.web_view.load(QUrl(url))
    
    def start_auto_update(self, interval_ms=30000):  # Update every 30 seconds
        """Start automatic map updates"""
        self.update_timer.start(interval_ms)
        
    def stop_auto_update(self):
        """Stop automatic map updates"""
        self.update_timer.stop()
        
    def zoom_in(self):
        """Zoom in on the web view"""
        current_zoom = self.web_view.zoomFactor()
        self.web_view.setZoomFactor(min(current_zoom * 1.2, 3.0))
        
    def zoom_out(self):
        """Zoom out on the web view"""
        current_zoom = self.web_view.zoomFactor()
        self.web_view.setZoomFactor(max(current_zoom / 1.2, 0.5))
        
    def reset_zoom(self):
        """Reset zoom to default"""
        self.web_view.setZoomFactor(1.0)
        
    def execute_javascript(self, script):
        """Execute JavaScript in the web view (useful for map interactions)"""
        self.web_view.page().runJavaScript(script)
        
    def get_current_url(self):
        """Get the current URL being displayed"""
        return self.web_view.url().toString()
        
    def go_back(self):
        """Navigate back in web view history"""
        if self.web_view.history().canGoBack():
            self.web_view.back()
            
    def go_forward(self):
        """Navigate forward in web view history"""
        if self.web_view.history().canGoForward():
            self.web_view.forward()
            
    def closeEvent(self, event):
        """Clean up when widget is closed"""
        self.stop_auto_update()
        super().closeEvent(event)