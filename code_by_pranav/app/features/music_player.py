import yt_dlp
from PyQt6.QtCore import QObject, QTimer, pyqtSignal, pyqtSlot, QThread
from ..vehicle_state import vehicle_state
from .. import config

class MusicWorker(QObject):
    playlist_ready = pyqtSignal(list); stream_info_ready = pyqtSignal(dict); error_occurred = pyqtSignal(str)
    @pyqtSlot(str)
    def fetch_playlist(self, url):
        ydl_opts = {'quiet': True, 'extract_flat': True, 'dump_single_json': True, 'playlist_items': '1-5'}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                info = ydl.extract_info(url, download=False); entries = info.get("entries", [])
                self.playlist_ready.emit(entries)
            except Exception as e: self.error_occurred.emit(f"Playlist Error: {e}")
    @pyqtSlot(str)
    def fetch_stream_url(self, video_url):
        ydl_opts = {'format': 'bestaudio/best', 'quiet': True}
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl: info = ydl.extract_info(video_url, download=False); self.stream_info_ready.emit(info)
        except Exception as e: self.error_occurred.emit(f"Stream Error: {e}")

class MusicPlayer(QObject):
    def __init__(self, parent=None):
        super().__init__(parent); self.player = None; self.song_list = []; self.current_song_index = 0; self._is_playing = False
        self.timer = QTimer(self); self.timer.setInterval(1000); self.timer.timeout.connect(self._update_status)
        self._setup_worker_thread(); self.worker.fetch_playlist(config.DEFAULT_PLAYLIST_URL)

    def _setup_worker_thread(self):
        self.thread = QThread(); self.worker = MusicWorker(); self.worker.moveToThread(self.thread)
        self.worker.playlist_ready.connect(self._on_playlist_ready)
        self.worker.stream_info_ready.connect(self._on_stream_info_ready)
        self.worker.error_occurred.connect(lambda e: print(f"Music Player Error: {e}"))
        self.thread.start()

    def _on_playlist_ready(self, entries):
        self.song_list = [e for e in entries if e and e.get("url")]; print(f"MusicPlayer: Loaded {len(self.song_list)} songs.")
        if self.song_list: vehicle_state.set_current_media(self.song_list[0].get('title', 'Playlist Loaded'), self.song_list[0].get('uploader', 'Ready to Play'))

    def _on_stream_info_ready(self, info):
        stream_url = info.get("url"); title = info.get('title', 'Unknown Title'); artist = info.get('uploader', 'Unknown Artist')
        if not stream_url: self.play_next(); return
        if self.player: self.player.stop()
        # self.player = vlc.MediaPlayer(stream_url); self.player.play(); self._is_playing = True
        self.timer.start(); vehicle_state.set_current_media(title, artist)

    def _play_song_by_index(self):
        if not self.song_list or not (0 <= self.current_song_index < len(self.song_list)): return
        self.worker.fetch_stream_url(self.song_list[self.current_song_index].get("url"))

    def play_pause(self):
        if not self._is_playing and not self.player and self.song_list: self._play_song_by_index()
        elif self.player: self.player.pause(); self._is_playing = self.player.is_playing()
    def play_next(self):
        if not self.song_list: return
        self.current_song_index = (self.current_song_index + 1) % len(self.song_list); self._play_song_by_index()
    def play_previous(self):
        if not self.song_list: return
        self.current_song_index = (self.current_song_index - 1) % len(self.song_list); self._play_song_by_index()
    def seek(self, pos):
        if self.player and self.player.is_seekable(): self.player.set_position(pos)
    def _update_status(self):
        if not self.player: return
        pos, length = self.player.get_time(), self.player.get_length()
        if length > 0: vehicle_state.media_progress_changed.emit(pos, length)
        # if self.player.get_state() == vlc.State.Ended: self.play_next()