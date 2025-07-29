# spectator_map.py
import sys
import json
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl, pyqtSlot, QTimer # Import QTimer
from PyQt6.QtWebChannel import QWebChannel

from app import config
from app.vehicle_state import vehicle_state

class SpectatorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Spectator Map")
        self.setGeometry(100, 100, 800, 600)

        # Setup the web view
        self.web_view = QWebEngineView()
        self.channel = QWebChannel()
        self.web_view.page().setWebChannel(self.channel)
        
        map_path = config.get_asset_path("map.html")
        self.web_view.setUrl(QUrl.fromLocalFile(map_path))
        self.setCentralWidget(self.web_view)

        # --- FIX: Use a timer to delay initialization ---
        # Wait 100ms after the window loads before connecting signals and syncing.
        QTimer.singleShot(100, self._initialize_and_sync)

    def _initialize_and_sync(self):
        """Connects to state signals and syncs the initial map view."""
        print("Spectator map initialized and syncing state.")
        # Connect to ALL relevant signals from vehicle_state
        vehicle_state.location_changed.connect(self.update_user_position)
        vehicle_state.start_marker_changed.connect(self.set_start_marker)
        vehicle_state.dest_marker_changed.connect(self.set_dest_marker)
        vehicle_state.route_changed.connect(self.draw_route)
        vehicle_state.map_cleared.connect(self.clear_map)
        
        # Apply the current map state when the window first loads
        self.sync_initial_state()

    def _run_js(self, script):
        self.web_view.page().runJavaScript(script)
        
    def sync_initial_state(self):
        """Applies the current map state from vehicle_state."""
        self.set_start_marker(vehicle_state.get_start_marker())
        self.set_dest_marker(vehicle_state.get_dest_marker())
        self.draw_route(vehicle_state.get_route_geometry())
        
        # Also sync the current live position if it exists
        loc = vehicle_state.get_location()
        if loc and loc.get('lat') != 0.0:
             self.update_user_position(loc['lat'], loc['lng'])

    @pyqtSlot(float, float)
    def update_user_position(self, lat, lng):
        self._run_js(f"mapApi.updateUserPosition({lat}, {lng});")

    @pyqtSlot(object)
    def set_start_marker(self, pos):
        if pos: self._run_js(f"mapApi.setStartMarker({pos['lat']}, {pos['lng']});")

    @pyqtSlot(object)
    def set_dest_marker(self, pos):
        if pos: self._run_js(f"mapApi.setDestinationMarker({pos['lat']}, {pos['lng']});")

    @pyqtSlot(object)
    def draw_route(self, geometry):
        if geometry: self._run_js(f"mapApi.drawRoute({json.dumps(geometry)});")

    @pyqtSlot()
    def clear_map(self):
        self._run_js("mapApi.clearMap();")