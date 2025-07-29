from PyQt6.QtCore import QObject, pyqtSignal

class VehicleState(QObject):
    _instance = None
    ac_state_changed = pyqtSignal(bool); ac_mode_changed = pyqtSignal(bool)
    fan_speed_changed = pyqtSignal(int); cabin_temp_changed = pyqtSignal(int)
    battery_percentage_changed = pyqtSignal(float); vehicle_speed_changed = pyqtSignal(float)
    location_changed = pyqtSignal(float, float); media_changed = pyqtSignal(dict)
    media_progress_changed = pyqtSignal(int, int)

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(VehicleState, cls).__new__(cls)
            cls._instance._init_state()
        return cls._instance

    def _init_state(self):
        self._ac_on = False; self._ac_auto_mode = True; self._fan_speed = 50; self._cabin_temp = 27
        self._battery_percentage =27.0; self._vehicle_speed = 0.0; self._location = {'lat': 0.0, 'lng': 0.0}
        self._current_media = {'title': 'Not Playing', 'artist': 'No Artist'}; self._music_player = None

    def is_ac_on(self): return self._ac_on
    def is_ac_auto(self): return self._ac_auto_mode
    def get_fan_speed(self): return self._fan_speed
    def get_cabin_temp(self): return self._cabin_temp
    def get_battery_percentage(self): return self._battery_percentage
    def get_vehicle_speed(self): return self._vehicle_speed
    def get_current_media(self): return self._current_media

    def set_music_player(self, player): self._music_player = player
    def set_current_media(self, title, artist): self._current_media = {'title': title, 'artist': artist}; self.media_changed.emit(self._current_media)
    def set_ac_on(self, is_on): self._ac_on = is_on; self.ac_state_changed.emit(is_on)
    def set_ac_auto(self, is_auto): self._ac_auto_mode = is_auto; self.ac_mode_changed.emit(is_auto)
    def set_fan_speed(self, speed): self._fan_speed = speed; self.fan_speed_changed.emit(speed)
    def set_cabin_temp(self, temp): self._cabin_temp = temp; self.cabin_temp_changed.emit(temp)
    def set_battery_percentage(self, p): self._battery_percentage = p; self.battery_percentage_changed.emit(p)
    def set_speed(self, s): self._vehicle_speed = s; self.vehicle_speed_changed.emit(s)
    def set_location(self, lat, lng): self._location = {'lat': lat, 'lng': lng}; self.location_changed.emit(lat, lng)

    def media_play_pause(self):
        if self._music_player: self._music_player.play_pause()
    def media_next(self):
        if self._music_player: self._music_player.play_next()
    def media_previous(self):
        if self._music_player: self._music_player.play_previous()
    def media_seek(self, position_ratio):
        if self._music_player: self._music_player.seek(position_ratio)

vehicle_state = VehicleState()