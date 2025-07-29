from PyQt6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QStackedWidget, QPushButton, QVBoxLayout)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSize

from . import config
from .vehicle_state import vehicle_state
from .features.music_player import MusicPlayer
from .views.dashboard_view import DashboardView
from .views.map_view import MapView
from .views.car_view import CarView
from .views.all_apps_view import AllAppsView
from .views.youtube_view import YouTubeView
from .views.yt_music_view import YouTubeMusicView

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TATA Automotive OS"); self.setMinimumSize(config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
        self.setStyleSheet(f"background-color: {config.MAIN_BACKGROUND_COLOR};")
        self.music_player = MusicPlayer(); vehicle_state.set_music_player(self.music_player)
        self.nav_buttons = {}; self.view_stack = QStackedWidget()
        self.views = {
            "dashboard": DashboardView(), "map": MapView(), "car": CarView(),
            "all_apps": AllAppsView(), "youtube": YouTubeView(), "yt_music": YouTubeMusicView(),
        }
        for view in self.views.values(): self.view_stack.addWidget(view)
        if self.views.get("all_apps"): self.views["all_apps"].view_change_requested.connect(self.switch_view)
        self.nav_bar = self._create_nav_bar()
        main_widget = QWidget(); main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(15, 15, 15, 15); main_layout.setSpacing(15)
        main_layout.addWidget(self.view_stack, 1); main_layout.addWidget(self.nav_bar)
        self.setCentralWidget(main_widget)
        self.switch_view("dashboard")

    def _create_nav_bar(self):
        nav_bar = QWidget(); nav_bar.setFixedWidth(80); nav_bar.setStyleSheet(f"background-color: {config.NAV_BAR_COLOR}; border-radius: 40px;")
        nav_layout = QVBoxLayout(nav_bar); nav_layout.setSpacing(20); nav_layout.addStretch()
        for name, conf in config.NAV_BUTTONS_CONFIG.items():
            button = self._create_nav_button(conf)
            button.clicked.connect(lambda checked, n=name: self.switch_view(n))
            nav_layout.addWidget(button); self.nav_buttons[name] = button
        nav_layout.addStretch(); return nav_bar

    def _create_nav_button(self, config_dict):
        button = QPushButton(); button.setIcon(QIcon(config_dict["icon_inactive"])); button.setIconSize(QSize(32, 32))
        button.setFixedSize(60, 60); button.setStyleSheet(f"background-color: {config_dict['color_inactive']}; border-radius: 30px;")
        return button

    def switch_view(self, name):
        target_view = self.views.get(name)
        if target_view:
            if hasattr(self.view_stack.currentWidget(), "hide_event"): self.view_stack.currentWidget().hide_event()
            self.view_stack.setCurrentWidget(target_view)
            if hasattr(target_view, "show_event"): target_view.show_event()
            self._update_nav_buttons(name)

    def _update_nav_buttons(self, active_name):
        for name, button in self.nav_buttons.items():
            if name in config.NAV_BUTTONS_CONFIG:
                conf = config.NAV_BUTTONS_CONFIG[name]
                if name == active_name:
                    button.setStyleSheet(f"background-color: {conf['color_active']}; border-radius: 30px;"); button.setIcon(QIcon(conf["icon_active"]))
                else:
                    button.setStyleSheet(f"background-color: {conf['color_inactive']}; border-radius: 30px;"); button.setIcon(QIcon(conf["icon_inactive"]))