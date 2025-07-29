import math
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QFrame
from PyQt6.QtGui import QPainter, QColor, QFont, QPen, QPixmap, QIcon
from PyQt6.QtCore import Qt, pyqtSlot, QPointF, QRectF, QSize

from .. import config
from ..vehicle_state import vehicle_state

class _DialWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent); self.speed = 0; self.battery = 0; self.fuel = 43; self.range = 157; self.setMinimumSize(350, 350)
    @pyqtSlot(float)
    def set_speed(self, speed): self.speed = int(speed); self.update()
    @pyqtSlot(float)
    def set_battery(self, battery): self.battery = int(battery); self.update()
    def paintEvent(self, event):
        painter = QPainter(self); painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        width, height, side = self.width(), self.height(), min(self.width(), self.height())
        self._draw_speedometer(painter, width, height, side); self._draw_info_dials(painter, width, height, side)
    
    def _draw_speedometer(self, painter, width, height, side):
        painter.save()

        # Define a scale for the dial's diameter (e.g., 80% of available space)
        dial_diameter = side * 0.90

        # Calculate the top-left 'x' to center the dial horizontally
        offset_x = (width - dial_diameter) / 2
        
        # Create the new, smaller bounding box for the arc
        dial_rect = QRectF(offset_x, height * 0.4, dial_diameter, dial_diameter)
        
        radius = dial_diameter / 2.0
        center = QPointF(dial_rect.center())
        
        # Draw Background Arc
        pen = QPen(QColor(50, 50, 70), 15)
        pen.setCapStyle(Qt.PenCapStyle.FlatCap)
        painter.setPen(pen)
        start_angle = 180 * 16
        span_angle = -180 * 16
        painter.drawArc(dial_rect.adjusted(20, 20, -20, -20), start_angle, span_angle)

        speed_angle = -int((self.speed / 180.0) * 180.0 * 16)

        # Draw glow layer first
        glow_pen = QPen(QColor(0, 191, 255, 30), 25)
        glow_pen.setCapStyle(Qt.PenCapStyle.FlatCap)
        painter.setPen(glow_pen)
        painter.drawArc(dial_rect.adjusted(20, 20, -20, -20), start_angle, speed_angle)
        
        # Draw main progress arc
        progress_pen = QPen(QColor(0, 191, 255), 15)
        progress_pen.setCapStyle(Qt.PenCapStyle.FlatCap)
        painter.setPen(progress_pen)
        painter.drawArc(dial_rect.adjusted(20, 20, -20, -20), start_angle, speed_angle)
        
        # Draw Speed Text
        painter.setPen(QColor(Qt.GlobalColor.white))
        font = QFont("Arial", 50, QFont.Weight.Bold)
        painter.setFont(font)
        painter.drawText(dial_rect, Qt.AlignmentFlag.AlignCenter, f"{self.speed}")
        
        font.setPointSize(18)
        painter.setFont(font)
        painter.drawText(dial_rect.adjusted(0, 70, 0, 0), Qt.AlignmentFlag.AlignCenter, "km/h")
        
        # Draw Tick Marks and Labels
        font.setPointSize(10)
        painter.setFont(font)
        painter.setPen(QColor(150, 150, 150))
        
        for i in range(0, 181, 20):
            angle_rad = math.radians(i - 180)
            
            x1 = center.x() + (radius - 15) * math.cos(angle_rad)
            y1 = center.y() + (radius - 15) * math.sin(angle_rad)
            x2 = center.x() + (radius - 25) * math.cos(angle_rad)
            y2 = center.y() + (radius - 25) * math.sin(angle_rad)
            painter.drawLine(int(x1), int(y1), int(x2), int(y2))
            
            label_x = center.x() + (radius - 40) * math.cos(angle_rad)
            label_y = center.y() + (radius - 40) * math.sin(angle_rad)
            painter.drawText(int(label_x - 10), int(label_y - 5), 20, 10, Qt.AlignmentFlag.AlignCenter, str(i))

        painter.restore()
        
    def _draw_info_dials(self, painter, width, height, side):
        painter.save(); dial_size = 70; arc_center = QPointF(width/2, height*0.45); arc_radius = width/3.5
        fuel_angle, bat_angle, ran_angle = 160, 90, 20
        fuel_x = arc_center.x() + arc_radius * math.cos(math.radians(fuel_angle)); fuel_y = arc_center.y() - arc_radius * math.sin(math.radians(fuel_angle))
        bat_x = arc_center.x() + arc_radius * math.cos(math.radians(bat_angle)); bat_y = arc_center.y() - arc_radius * math.sin(math.radians(bat_angle))
        ran_x = arc_center.x() + arc_radius * math.cos(math.radians(ran_angle)); ran_y = arc_center.y() - arc_radius * math.sin(math.radians(ran_angle))
        fuel_r = QRectF(fuel_x - dial_size/2, fuel_y - dial_size/2, dial_size, dial_size); bat_r = QRectF(bat_x - dial_size/2, bat_y - dial_size/2, dial_size, dial_size); ran_r = QRectF(ran_x - dial_size/2, ran_y - dial_size/2, dial_size, dial_size)
        self._draw_single_dial(painter, fuel_r, QColor(0, 191, 255), self.fuel, "Fuel", "💧"); 
        self._draw_single_dial(painter, bat_r, QColor(34, 177, 76), self.battery, "Battery", "🔋");
        self._draw_single_dial(painter, ran_r, QColor(0, 191, 255), self.range, "Range", "📍")
        painter.restore()
    def _draw_single_dial(self, painter, rect, color, value, text, emoji):
        painter.save(); 
        painter.setPen(QPen(QColor(50, 50, 70), 4)); 
        painter.drawEllipse(rect)
        start_angle = 90 * 16; 
        percentage = (value / 500.0) if text == "Range" else (value / 100.0); 
        span_angle = -int(percentage * 360 * 16)
        glow_pen = QPen(QColor(color.red(), color.green(), color.blue(), 80), 8); glow_pen.setCapStyle(Qt.PenCapStyle.RoundCap); 
        painter.setPen(glow_pen)
        painter.drawArc(rect, start_angle, span_angle)
        progress_pen = QPen(color, 4);
        progress_pen.setCapStyle(Qt.PenCapStyle.RoundCap); 
        painter.setPen(progress_pen)
        painter.drawArc(rect, start_angle, span_angle)
        painter.setPen(QColor(Qt.GlobalColor.white)); 
        font = QFont("Arial", 12, QFont.Weight.Bold); painter.setFont(font)
        if text == "Range": 
            painter.drawText(rect.adjusted(0, 15, 0,10), Qt.AlignmentFlag.AlignCenter, f"{value} km")
        else: 
            painter.drawText(rect.adjusted(0, 15, 0,10), Qt.AlignmentFlag.AlignCenter, f"{value}%")
        font.setPointSize(18); 
        painter.setFont(font); 
        painter.drawText(rect.adjusted(0, 15, 0,-35), Qt.AlignmentFlag.AlignCenter, emoji); 
        painter.restore()

class CarInfoWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent); 
        self.dial_widget = _DialWidget()
        vehicle_state.vehicle_speed_changed.connect(self.dial_widget.set_speed)
        vehicle_state.battery_percentage_changed.connect(self.dial_widget.set_battery)
        self.dial_widget.set_speed(int(vehicle_state.get_vehicle_speed())); 
        self.dial_widget.set_battery(int(vehicle_state.get_battery_percentage()))
        main_layout = QVBoxLayout(self); 
        # main_layout.setSpacing(17);
        main_layout.setSpacing(0);
        
        title = QLabel("Genesis G80 Hybrid");
        title.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignHCenter); 
        title.setStyleSheet("color: white;"); 
        title.setMargin(15);
        
        car_layout = QHBoxLayout(); 
        car_image = QLabel()
        car_pixmap = QPixmap(config.get_asset_path("Genesis_G80_Hybrid.png"))
        if not car_pixmap.isNull(): 
            car_image.setPixmap(car_pixmap.scaledToWidth(400, Qt.TransformationMode.SmoothTransformation))
        else: 
            car_image.setText("Car Image Not Found"); 
            car_image.setStyleSheet("color: grey;")
        car_layout.addWidget(car_image, alignment=Qt.AlignmentFlag.AlignCenter); 
        main_layout.addWidget(title); 
        main_layout.addLayout(car_layout); 
        main_layout.addWidget(self.dial_widget)
        
        
      










