import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineSettings
from PyQt6.QtCore import QUrl

class MapWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Create web view
        self.view = QWebEngineView()
        
        # Get the page and settings
        page = self.view.page()
        settings = page.settings()
        
        # Enable geolocation and other required features
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessFileUrls, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalStorageEnabled, True)
        
        # Handle permission requests (crucial for geolocation)
        page.featurePermissionRequested.connect(self.handle_permission_request)
        
        # Load the FastAPI backend URL
        url = QUrl("http://127.0.0.1:8000/")
        self.view.load(url)
        
        layout.addWidget(self.view)
        self.setLayout(layout)
        self.setWindowTitle("Map Viewer with Geolocation")
        self.resize(1200, 800)
    
    def handle_permission_request(self, origin, permission):
        """Handle permission requests, especially for geolocation"""
        from PyQt6.QtWebEngineCore import QWebEnginePage
        
        # Grant permission for geolocation
        if permission == QWebEnginePage.Feature.Geolocation:
            self.view.page().setFeaturePermission(
                origin, 
                permission, 
                QWebEnginePage.PermissionPolicy.PermissionGrantedByUser
            )
            print(f"Granted geolocation permission for {origin.toString()}")
        else:
            # Grant other permissions as needed
            self.view.page().setFeaturePermission(
                origin, 
                permission, 
                QWebEnginePage.PermissionPolicy.PermissionGrantedByUser
            )
            print(f"Granted permission {permission} for {origin.toString()}")

def main():
    app = QApplication(sys.argv)
    
    # Set application name for better permission handling
    app.setApplicationName("Map Viewer")
    app.setOrganizationName("YourOrganization")
    
    window = MapWidget()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()