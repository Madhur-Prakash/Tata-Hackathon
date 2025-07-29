# app/views/dashboard_view.py
from PyQt6.QtWidgets import QWidget, QGridLayout
from PyQt6.QtCore import Qt

from .. import config
from ..vehicle_state import vehicle_state
from ..features.weather import WeatherWidget
from ..widgets.media_widget import MediaWidget
from ..widgets.map_preview_widget import MapPreviewWidget
from ..widgets.car_info_widget import CarInfoWidget

class DashboardView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        layout = QGridLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        # Create instances of all widgets for the dashboard
        car_info_widget = CarInfoWidget()
        self.map_preview = MapPreviewWidget()
        media_widget = MediaWidget()
        self.weather_widget = WeatherWidget()
        
        # Connect the map preview to the central vehicle state for live updates
        # vehicle_state.location_changed.connect(self.map_preview.update_location)

        # Add widgets to the grid layout
        layout.addWidget(car_info_widget, 0, 0, 2, 1)
        layout.addWidget(self.map_preview, 0, 1, 1, 2)
        layout.addWidget(media_widget, 1, 1, 1, 1)
        layout.addWidget(self.weather_widget, 1, 2, 1, 1)

    def update_map_preview(self, pixmap):
        """A public method for the MainWindow to call to update the snapshot."""
        self.map_preview.set_snapshot(pixmap)

    def show_event(self):
        """Called when the view becomes visible to start background tasks."""
        self.weather_widget.start_updates()

    def hide_event(self):
        """Called when the view is hidden to stop background tasks."""
        self.weather_widget.stop_updates()






