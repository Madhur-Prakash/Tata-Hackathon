# app/views/car_view.py
from PyQt6.QtWidgets import (QWidget, QHBoxLayout, QFrame, QVBoxLayout, QLabel, 
                             QSlider, QRadioButton, QButtonGroup)
from PyQt6.QtGui import (QPixmap, QColor, QImage, QPainter, QBrush, 
                         QRadialGradient, QFont, QIcon)
from PyQt6.QtCore import Qt, QPointF, QSize, pyqtSlot

from .. import config
from ..vehicle_state import vehicle_state
from ..widgets.toggle_button import ToggleButton

class CarView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.car_pixmap = QPixmap(config.get_asset_path("Car_Top_V2.png"))

        if self.car_pixmap.isNull():
            self._setup_error_ui()
        else:
            self._setup_ui()

    def _setup_error_ui(self):
        self.setLayout(QVBoxLayout())
        error_label = QLabel("Error: Car image asset not found.")
        error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout().addWidget(error_label)

    def _setup_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(15)

        left_panel = self._create_left_panel()
        right_panel = self._create_right_panel()

        main_layout.addWidget(left_panel, 2)
        main_layout.addWidget(right_panel, 3)
        
        # Connect UI controls to the central vehicle_state
        self.ac_toggle.button.toggled.connect(vehicle_state.set_ac_on)
        self.mode_toggle.button.toggled.connect(vehicle_state.set_ac_auto)
        self.temp_slider.valueChanged.connect(vehicle_state.set_cabin_temp)
        self.fan_slider.valueChanged.connect(vehicle_state.set_fan_speed)

        # Connect vehicle_state signals back to the UI widgets to keep them in sync
        vehicle_state.ac_state_changed.connect(self.ac_toggle.button.setChecked)
        vehicle_state.ac_mode_changed.connect(self.mode_toggle.button.setChecked)
        vehicle_state.cabin_temp_changed.connect(self.temp_slider.setValue)
        vehicle_state.fan_speed_changed.connect(self.fan_slider.setValue)
        vehicle_state.cabin_temp_changed.connect(self.update_gradient)
        
        # Initialize the view with the current state
        self.update_gradient(vehicle_state.get_cabin_temp())

    def _create_left_panel(self):
        panel = QFrame()
        panel.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #444, stop:1 #222);
                border-radius: 15px;
            }
        """)
        layout = QVBoxLayout(panel)
        self.image_label = QLabel(alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.image_label)
        return panel
        
    def _create_right_panel(self):
        """Creates the right panel with all the climate controls."""
        panel = QFrame()
        panel.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #000, stop:1 #444);
                border-radius: 15px;
            }
            QLabel { color: white; }
        """)
        main_layout = QVBoxLayout(panel)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(25)

        # --- Row 1: A/C Controls ---
        ac_row = QHBoxLayout()
        ac_row.setSpacing(20)
        ac_label = QLabel("A/C")
        ac_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        ac_label.setFixedHeight(35)
        self.ac_toggle = ToggleButton(on_text="On", off_text="Off", on_color="#00cc99", off_color="#2A2A2A")
        self.ac_toggle.setFixedSize(80, 30)
        self.mode_toggle = ToggleButton(on_text="Auto", off_text="Manual", on_color="#0066cc", off_color="#2A2A2A")
        self.mode_toggle.setFixedSize(100, 30)
        self.ac_toggle.button.setChecked(vehicle_state.is_ac_on())
        self.mode_toggle.button.setChecked(vehicle_state.is_ac_auto())
        ac_row.addWidget(ac_label)
        ac_row.addWidget(self.ac_toggle)
        ac_row.addStretch()
        ac_row.addWidget(self.mode_toggle)
        main_layout.addLayout(ac_row)
        
        # --- Row 2: Fan Controls ---
        fan_layout = QVBoxLayout()
        fan_layout.setSpacing(0) 
        fan_title = QLabel("Fan Speed",alignment=Qt.AlignmentFlag.AlignCenter)
        fan_title.setFont(QFont("Arial", 16))
        fan_title.setFixedSize(95, 25)
        fan_layout.addWidget(fan_title, alignment=Qt.AlignmentFlag.AlignLeft)
        fan_row = QHBoxLayout()
        fan_row.setSpacing(10) 
        fan_icon = QLabel()
        fan_icon.setPixmap(QPixmap(config.get_asset_path("fan.png")).scaled(QSize(45, 45)))
        fan_row.addWidget(fan_icon)
        self.fan_slider = GradientSlider()
        self.fan_slider.setRange(0, 100)
        self.fan_slider.setValue(vehicle_state.get_fan_speed())
        fan_row.addWidget(self.fan_slider)
        fan_layout.addLayout(fan_row)
        main_layout.addLayout(fan_layout)

        # --- Row 3: Temperature Slider ---
        temp_layout = QVBoxLayout()
        temp_layout.setSpacing(0) 
        temp_title = QLabel("Temperature",alignment=Qt.AlignmentFlag.AlignCenter)
        temp_title.setFont(QFont("Arial", 16))
        temp_title.setFixedSize(100, 25)
        temp_layout.addWidget(temp_title, alignment=Qt.AlignmentFlag.AlignLeft)
        temp_row = QHBoxLayout()
        temp_row.setSpacing(10)
        self.temp_slider = QSlider(Qt.Orientation.Horizontal)
        self.temp_slider.setRange(16, 32)
        self.temp_slider.setValue(vehicle_state.get_cabin_temp())
        self.temp_slider.setFixedHeight(30)
        self.temp_slider.setStyleSheet("""
            QSlider { background: transparent; }
            /* Glossy groove using gradient for sheen effect */
            QSlider::groove:horizontal {
                border: none; height: 12px; border-radius: 6px;
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgb(0, 153, 255),
                    stop:0.5 rgb(180, 120, 80),
                    stop:1 rgb(255, 85, 0)
                );
                margin: 0px;
            }
            /* Handle with faux gloss using radial gradient */
            QSlider::handle:horizontal {
                background: qradialgradient(
                    cx:0.5, cy:0.4, radius:0.6,
                    fx:0.5, fy:0.4,
                    stop:0 white,
                    stop:0.5 rgb(230, 230, 230),
                    stop:1 rgb(180, 180, 180)
                );
                border: 1px solid gray; width: 22px; height: 22px; margin: -7px 0px; border-radius: 11px;
            }
        """)
        temp_value_label = QLabel(f"{self.temp_slider.value()}°C",alignment = Qt.AlignmentFlag.AlignCenter)
        temp_value_label.setFont(QFont("Arial", 25, QFont.Weight.Bold))
        temp_value_label.setFixedWidth(60)
        temp_row.addWidget(temp_value_label)
        temp_row.addWidget(self.temp_slider)
        self.temp_slider.valueChanged.connect(lambda v: temp_value_label.setText(f"{v}°C"))
        
        temp_layout.addLayout(temp_row)
        main_layout.addLayout(temp_layout)
        
        # --- Row 4, 5, 6: Airflow Controls from Code 1 ---
        togg_layout = QVBoxLayout()
        togg_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        # togg_layout.setSpacing(10)
        
        airflow_buttons = [("Air_1.png", "Face"), ("Air_2.png", "Face & Feet"), ("Air_3.png", "Feet"), ("Air_4.png", "Defrost & Feet")]
        defrost_buttons = [("Defrost_F.png", "Front Defrost"), ("Defrost_R.png", "Rear Defrost")]
        circulation_buttons = [("Air_F.png", "Fresh Air"), ("Air_R.png", "Recirculate")]

        airflow_row = self._create_button_row(airflow_buttons, "Air_2.png", title="Airflow")
        
        sub_row = QHBoxLayout()
        sub_row.addLayout(self._create_button_row(defrost_buttons, "Defrost_F.png", title="Defrost"))
        sub_row.addLayout(self._create_button_row(circulation_buttons, "Air_R.png", title="Circulation"))
        
        togg_layout.addLayout(airflow_row,stretch=1)
        togg_layout.addLayout(sub_row,stretch=1)
        main_layout.addLayout(togg_layout)
        
        main_layout.addStretch()
        return panel

    def _create_button_row(self, button_info, default_icon, title=""):
        v_layout = QVBoxLayout()
        # v_layout.setSpacing(5)
        v_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        if title:
            title_label = QLabel(title)
            title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            title_label.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
            title_label.setFixedHeight(40)
            v_layout.addWidget(title_label)

        h_layout = QHBoxLayout()
        h_layout.setSpacing(85)
        h_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        button_group = QButtonGroup(self)
        button_group.setExclusive(True)
        
        for icon_name, tooltip in button_info:
            radio = QRadioButton()
            radio.setIcon(QIcon(config.get_asset_path(icon_name)))
            # radio.setIconSize(QSize(64, 64))
            radio.setIconSize(QSize(80, 80))
            radio.setToolTip(tooltip)
            radio.setStyleSheet("""
                QRadioButton::indicator { width: 0px; height: 0px; }
                QRadioButton { border: none; padding: 5px; }
                QRadioButton:checked {
                    background-color: rgba(0, 120, 255, 80);
                    border-radius: 8px;
                    border: 2px solid #0078FF;
                }
            """)
            if icon_name == default_icon:
                radio.setChecked(True)
            h_layout.addWidget(radio)
            button_group.addButton(radio)
        
        v_layout.addLayout(h_layout)
        return v_layout

    @pyqtSlot(int)
    def update_gradient(self, value):
        normalized_value = (value - 16) / (32 - 16)
        color = self._interpolate_color(QColor(0, 128, 255), QColor(255, 102, 0), normalized_value)
        gradient_image = self._apply_gradient_to_image(self.car_pixmap, color)
        self.image_label.setPixmap(QPixmap.fromImage(gradient_image))

    def _apply_gradient_to_image(self, base_pixmap, color):
        image = base_pixmap.toImage().convertToFormat(QImage.Format.Format_ARGB32)
        width, height = image.width(), image.height()
        gradient_image = QImage(width, height, QImage.Format.Format_ARGB32)
        gradient_image.fill(Qt.GlobalColor.transparent)
        painter = QPainter(gradient_image)
        painter.drawImage(0, 0, image)
        center = QPointF(width / 2, height / 2)
        radius = min(width, height) * 0.6
        radial_gradient = QRadialGradient(center, radius * 1.2)
        radial_gradient.setColorAt(0, color)
        radial_gradient.setColorAt(1, Qt.GlobalColor.transparent)
        painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceAtop)
        painter.setBrush(QBrush(radial_gradient))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(center, radius, radius * 1.1)
        painter.end()
        return gradient_image

    def _interpolate_color(self, color1, color2, t):
        r = int(color1.red() + (color2.red() - color1.red()) * t)
        g = int(color1.green() + (color2.green() - color1.green()) * t)
        b = int(color1.blue() + (color2.blue() - color1.blue()) * t)
        return QColor(r, g, b)
    
class GradientSlider(QSlider):
    def __init__(self, orientation=Qt.Orientation.Horizontal, parent=None):
        super().__init__(orientation, parent)
        self.setRange(0, 100)
        self.setValue(50)
        self.setFixedHeight(30)
        self.valueChanged.connect(self.update_gradient)
        self.update_gradient(self.value())

    def update_gradient(self, value):
        percent = (value - self.minimum()) / (self.maximum() - self.minimum())

        self.setStyleSheet(f"""
            QSlider {{
                background: transparent;
            }}
            QSlider::groove:horizontal {{
                height: 10px;
                border-radius: 5px;
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 white,
                    stop:{percent:.2f} #007BFF,
                    stop:{percent:.2f} rgba(255, 255, 255, 30),
                    stop:1 rgba(255, 255, 255, 20)
                );
            }}
            QSlider::handle:horizontal {{
                background: white;
                border: 2px solid #007BFF;
                width: 20px;
                height: 20px;
                margin: -6px 0px;
                border-radius: 10px;
            }}
        """)