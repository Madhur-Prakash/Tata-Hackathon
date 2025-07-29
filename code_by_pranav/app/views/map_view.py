# app/views/map_view.py
import json
import requests
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLineEdit, QLabel, QGroupBox, QCheckBox)
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineSettings, QWebEnginePage
from PyQt6.QtCore import QUrl, QObject, pyqtSlot, QTimer, QThread, pyqtSignal
from PyQt6.QtWebChannel import QWebChannel

from .. import config
from ..vehicle_state import vehicle_state

# --- Worker for background network tasks ---
class MapWorker(QObject):
    search_result = pyqtSignal(dict, str) # Emits result and an identifier ('start' or 'dest')
    route_result = pyqtSignal(dict)
    error = pyqtSignal(str)

    @pyqtSlot(str, dict, str)
    def perform_search(self, query, live_location, search_type):
        try:
            base_url = "https://nominatim.openstreetmap.org/search"
            params = {'q': query, 'format': 'json', 'limit': 1}
            if live_location:
                l = live_location
                params['viewbox'] = f"{l['lng']-1},{l['lat']+1},{l['lng']+1},{l['lat']-1}"
                params['bounded'] = 1
            response = requests.get(base_url, params=params, headers={'User-Agent': 'TataEVApp/1.0'}, timeout=10)
            response.raise_for_status()
            locations = response.json()
            if locations:
                self.search_result.emit(locations[0], search_type)
            else:
                self.error.emit("Location not found.")
        except Exception as e:
            self.error.emit(f"Search Error: {e}")

    @pyqtSlot(list, list)
    def get_route(self, start_coords, end_coords):
        try:
            url = f"http://router.project-osrm.org/route/v1/driving/{start_coords[0]},{start_coords[1]};{end_coords[0]},{end_coords[1]}?overview=full&geometries=geojson"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            route_data = response.json()
            if route_data.get('code') == 'Ok':
                self.route_result.emit(route_data)
            else:
                self.error.emit("Could not find a route.")
        except Exception as e:
            self.error.emit(f"Routing Error: {e}")

# --- Bridge for JS to call Python ---
class MapBridge(QObject):
    def __init__(self, parent_view):
        super().__init__(parent_view)
        self.parent_view = parent_view
    @pyqtSlot(float, float, float)
    def update_location_data(self, lat, lng, speed_kmh):
        self.parent_view.live_location = {'lat': lat, 'lng': lng}
        if not self.parent_view.start_location:
            self.parent_view.start_location = self.parent_view.live_location
        vehicle_state.set_speed(speed_kmh)
        vehicle_state.set_location(lat, lng)

# --- Main MapView Widget ---
class MapView(QWidget):
    search_requested = pyqtSignal(str, dict, str)
    route_requested = pyqtSignal(list, list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_state_and_timers()
        self._setup_ui()
        self._setup_worker_thread()
        self._setup_bridge_and_load()
        self._connect_signals()

    def _setup_state_and_timers(self):
        self.start_location, self.destination_location, self.live_location = None, None, None
        self.route_coordinates, self.simulation_index = [], 0
        self.simulation_timer = QTimer(self)
        self.simulation_timer.setInterval(1000)

    def _setup_ui(self):
        main_layout = QHBoxLayout(self); main_layout.setContentsMargins(0, 0, 0, 0)
        controls_container = QWidget(); controls_container.setFixedWidth(350); controls_container.setStyleSheet("color: white; padding: 10px;")
        controls_layout = QVBoxLayout(controls_container)
        start_group = QGroupBox("Start Location"); start_layout = QVBoxLayout(start_group)
        self.use_custom_start_checkbox = QCheckBox("Set Custom Start")
        self.start_input_container = QWidget()
        start_input_layout = QVBoxLayout(self.start_input_container)
        self.start_input = QLineEdit(); self.start_input.setPlaceholderText("Search start location...")
        self.start_search_button = QPushButton("Search Start")
        start_input_layout.addWidget(self.start_input); start_input_layout.addWidget(self.start_search_button)
        self.start_input_container.setVisible(False)
        start_layout.addWidget(self.use_custom_start_checkbox); start_layout.addWidget(self.start_input_container)
        controls_layout.addWidget(start_group)
        dest_group = QGroupBox("Destination"); dest_layout = QVBoxLayout(dest_group)
        self.dest_input = QLineEdit(); self.dest_input.setPlaceholderText("Search destination...")
        self.dest_search_button = QPushButton("Search Destination")
        dest_layout.addWidget(self.dest_input); dest_layout.addWidget(self.dest_search_button)
        controls_layout.addWidget(dest_group)
        style_group = QGroupBox("Map Style"); style_layout = QHBoxLayout(style_group)
        self.theme_toggle_button = QPushButton("Light/Dark Theme"); self.view_toggle_button = QPushButton("Toggle View")
        style_layout.addWidget(self.theme_toggle_button); style_layout.addWidget(self.view_toggle_button)
        controls_layout.addWidget(style_group)
        actions_group = QGroupBox("Actions"); actions_layout = QHBoxLayout(actions_group)
        self.start_nav_button = QPushButton("Start Navigation"); self.start_nav_button.setStyleSheet("background-color: #4CAF50; color: white;")
        self.clear_map_button = QPushButton("Clear Map"); self.clear_map_button.setStyleSheet("background-color: #D32F2F; color: white;")
        actions_layout.addWidget(self.start_nav_button); actions_layout.addWidget(self.clear_map_button)
        controls_layout.addWidget(actions_group)
        sim_group = QGroupBox("Simulation"); sim_layout = QHBoxLayout(sim_group)
        self.simulate_button = QPushButton("Start Simulation"); self.simulate_button.setCheckable(True)
        sim_layout.addWidget(self.simulate_button)
        controls_layout.addWidget(sim_group)
        status_group = QGroupBox("Status"); status_layout = QVBoxLayout(status_group)
        self.speed_label = QLabel(f"🚗 Speed: {vehicle_state.get_vehicle_speed():.1f} km/h")
        self.battery_label = QLabel(f"🔋 Battery: {vehicle_state.get_battery_percentage():.1f}%")
        self.status_label = QLabel("Map is ready.")
        status_layout.addWidget(self.speed_label); status_layout.addWidget(self.battery_label); status_layout.addWidget(self.status_label)
        controls_layout.addWidget(status_group); controls_layout.addStretch()
        self.web_view = QWebEngineView()
        page = self.web_view.page(); settings = page.settings()
        settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, True)
        page.featurePermissionRequested.connect(self._handle_permission_request)
        main_layout.addWidget(controls_container); main_layout.addWidget(self.web_view, 1)

    def _setup_worker_thread(self):
        self.thread = QThread()
        self.worker = MapWorker()
        self.worker.moveToThread(self.thread)
        self.search_requested.connect(self.worker.perform_search)
        self.route_requested.connect(self.worker.get_route)
        self.worker.search_result.connect(self._on_search_result)
        self.worker.route_result.connect(self._on_route_result)
        self.worker.error.connect(lambda msg: self.update_status_label(msg, "error"))
        self.thread.start()
        
    def _setup_bridge_and_load(self):
        self.bridge = MapBridge(self)
        self.channel = QWebChannel()
        self.web_view.page().setWebChannel(self.channel)
        self.channel.registerObject("py_bridge", self.bridge)
        self.web_view.loadFinished.connect(lambda: self._run_js("mapApi.initializeMap(28.5432, 77.3327);"))
        map_path = config.get_asset_path("map.html")
        self.web_view.setUrl(QUrl.fromLocalFile(map_path))

    def _connect_signals(self):
        self.use_custom_start_checkbox.toggled.connect(self.start_input_container.setVisible)
        self.start_search_button.clicked.connect(lambda: self.search_requested.emit(self.start_input.text(), self.live_location, "start"))
        self.dest_search_button.clicked.connect(lambda: self.search_requested.emit(self.dest_input.text(), self.live_location, "dest"))
        self.theme_toggle_button.clicked.connect(lambda: self._run_js("mapApi.toggleTheme();"))
        self.view_toggle_button.clicked.connect(lambda: self._run_js("mapApi.toggleView();"))
        self.start_nav_button.clicked.connect(lambda: self._run_js("mapApi.startNavigation();"))
        self.simulate_button.toggled.connect(self._toggle_simulation)
        self.clear_map_button.clicked.connect(self.clear_map)
        self.simulation_timer.timeout.connect(self._simulate_step)
        vehicle_state.vehicle_speed_changed.connect(self.update_speed_label)
        vehicle_state.battery_percentage_changed.connect(self.update_battery_label)

    def _run_js(self, script): self.web_view.page().runJavaScript(script)

    @pyqtSlot(dict, str)
    def _on_search_result(self, loc, search_type):
        pos = {'lat': float(loc['lat']), 'lng': float(loc['lon'])}
        if search_type == 'start':
            self.start_location = pos
            self.update_status_label(f"Start set: {loc['display_name'][:30]}...", "success")
            self._run_js(f"mapApi.setStartMarker({pos['lat']}, {pos['lng']});")
        else:
            self.destination_location = pos
            self.update_status_label(f"Destination set: {loc['display_name'][:30]}...", "success")
            self._run_js(f"mapApi.setDestinationMarker({pos['lat']}, {pos['lng']});")
        self._draw_route()

    @pyqtSlot(dict)
    def _on_route_result(self, route_data):
        geometry = json.dumps(route_data['routes'][0]['geometry'])
        self.route_coordinates = route_data['routes'][0]['geometry']['coordinates']
        self._run_js(f"mapApi.drawRoute({geometry});")
        self.update_status_label("Route drawn on map.", "success")
        
    def _draw_route(self):
        start_loc = self.start_location if self.use_custom_start_checkbox.isChecked() else self.live_location
        if start_loc and self.destination_location:
            self.route_requested.emit([start_loc['lng'], start_loc['lat']], [self.destination_location['lng'], self.destination_location['lat']])

    def clear_map(self):
        self.start_location, self.destination_location, self.route_coordinates, self.simulation_index = None, None, [], 0
        self.dest_input.clear(); self.start_input.clear()
        if self.simulation_timer.isActive(): self._toggle_simulation(False)
        self._run_js("mapApi.clearMap()")
        self.update_status_label("Map cleared.", "success")

    def _toggle_simulation(self, checked):
        if checked:
            if not self.route_coordinates:
                self.update_status_label("Draw a route to start.", "error"); self.simulate_button.setChecked(False); return
            self.simulation_index = 0; self.simulation_timer.start(); self.simulate_button.setText("Stop Simulation")
        else:
            self.simulation_timer.stop(); self.simulate_button.setText("Start Simulation")

    def _simulate_step(self):
        if self.simulation_index >= len(self.route_coordinates):
            self._toggle_simulation(False); self.update_status_label("Simulation finished.", "success"); return
        lng, lat = self.route_coordinates[self.simulation_index]
        self._run_js(f"mapApi.updateUserPosition({lat}, {lng});")
        vehicle_state.set_speed(45.0); new_battery = max(0, vehicle_state.get_battery_percentage() - 0.1); vehicle_state.set_battery_percentage(round(new_battery, 1))
        self.simulation_index = min(self.simulation_index + 5, len(self.route_coordinates))

    def update_status_label(self, message, msg_type):
        color = "#66FF66" if msg_type == "success" else "#FF6666" if msg_type == "error" else "white"
        self.status_label.setText(message); self.status_label.setStyleSheet(f"color: {color};")
        
    def _handle_permission_request(self, origin, feature):
        if feature == QWebEnginePage.Feature.Geolocation:
            self.web_view.page().setFeaturePermission(origin, feature, QWebEnginePage.PermissionPolicy.PermissionGrantedByUser)
            
    def update_backend(self):
        if not self.live_location: return
        try:
            payload = {"lat": self.live_location['lat'], "lng": self.live_location['lng'], "batteryLevel": vehicle_state.get_battery_percentage()}
            url = "http://127.0.0.1:8000/api/location/update"
            requests.post(url, json=payload, timeout=5).raise_for_status()
        except Exception as e:
            print(f"ERROR: Backend update failed: {e}")
            
    @pyqtSlot(float)
    def update_speed_label(self, speed): self.speed_label.setText(f"🚗 Speed: {speed:.1f} km/h")
    @pyqtSlot(float)
    def update_battery_label(self, p): self.battery_label.setText(f"🔋 Battery: {p:.1f}%")