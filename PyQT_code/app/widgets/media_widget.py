# app/widgets/media_widget.py
# --- 1. Import QFrame ---
from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QSlider, QFrame
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon
from ..vehicle_state import vehicle_state
from .. import config

# --- 2. Change inheritance from QWidget to QFrame ---
class MediaWidget(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setFixedSize(350, 300)
        
        # --- 3. Give the frame an object name for specific styling ---
        self.setObjectName("MediaWidgetFrame")
        self.setStyleSheet(f"""
            QFrame#MediaWidgetFrame {{
                background-color: {config.WIDGET_BACKGROUND_COLOR};
                border-radius: 10px;
            }}
            QLabel, QPushButton {{
                background-color: transparent;
                color: white;
            }}
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(5)
        
        self.song_title = QLabel("Not Playing")
        self.song_title.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.song_title.setWordWrap(True)
        self.song_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.artist_label = QLabel("No Artist")
        self.artist_label.setStyleSheet("color: gray; font-size: 16px;")
        
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(0, 1000)
        self.slider.setStyleSheet("""
            /* Style the main slider widget itself */
            QSlider {
                background: transparent;
                border: none;
            }
            /* Style the track (the groove) */
            QSlider::groove:horizontal {
                background: #404040;
                border: none; /* Add this */
                height: 6px;
                border-radius: 3px;
            }
            /* Style the handle */
            QSlider::handle:horizontal {
                background: white;
                border: none; /* Keep this */
                width: 12px;
                margin: -4px 0;
                border-radius: 6px;
            }
            /* Style the filled part of the track */
            QSlider::sub-page:horizontal {
                background: #1DB954;
                border: none; /* Add this */
                height: 6px; /* Match groove height */
                border-radius: 3px; /* Match groove radius */
            }
        """)
        
        controls_layout = QHBoxLayout()
        self.prev_btn = QPushButton(icon=QIcon(config.get_asset_path("prev.png")))
        self.play_btn = QPushButton(icon=QIcon(config.get_asset_path("play.png")))
        self.next_btn = QPushButton(icon=QIcon(config.get_asset_path("next.png")))
        
        for btn in [self.prev_btn, self.next_btn]:
            btn.setIconSize(QSize(50, 50))
            btn.setFixedSize(QSize(80, 80))
            btn.setStyleSheet("border: none;")
        
        for btn in [self.play_btn ]:
            btn.setIconSize(QSize(80, 80))
            btn.setFixedSize(QSize(80, 80))
            btn.setStyleSheet("border: none;")
            
        controls_layout.addWidget(self.prev_btn)
        controls_layout.addWidget(self.play_btn)
        controls_layout.addWidget(self.next_btn)
        
        layout.addWidget(self.song_title, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.artist_label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.slider)
        layout.addLayout(controls_layout)
        
        # Connect to vehicle state
        vehicle_state.media_changed.connect(self.update_media_info)
        vehicle_state.media_progress_changed.connect(self.update_progress)
        
        self.play_btn.clicked.connect(vehicle_state.media_play_pause)
        self.next_btn.clicked.connect(vehicle_state.media_next)
        self.prev_btn.clicked.connect(vehicle_state.media_previous)
        self.slider.sliderMoved.connect(self.seek_media)

    def update_media_info(self, media_dict):
        self.song_title.setText(media_dict.get('title', 'Not Playing'))
        self.artist_label.setText(media_dict.get('artist', 'No Artist'))

    def update_progress(self, position_ms, duration_ms):
        if duration_ms > 0 and not self.slider.isSliderDown():
            progress = int((position_ms / duration_ms) * 1000)
            self.slider.setValue(progress)
            
    def seek_media(self, value):
        position_ratio = value / 1000.0
        vehicle_state.media_seek(position_ratio)