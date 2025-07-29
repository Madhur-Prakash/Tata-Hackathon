import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, 'app', 'assets')

def get_asset_path(filename):
    return os.path.join(ASSETS_DIR, filename)

WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
SPLASH_SCREEN_TIMEOUT = 2000

MAIN_BACKGROUND_COLOR = "#17161A"
NAV_BAR_COLOR = "#1F1E24"
WIDGET_BACKGROUND_COLOR = "#36363F"

DEFAULT_PLAYLIST_URL = "https://music.youtube.com/playlist?list=RDCLAK5uy_kpxnNxJpPZjLKbL9WgvrPuErWkUxMP6x4"

NAV_BUTTONS_CONFIG = {
    "dashboard": {"icon_active": get_asset_path("Home_b.png"), "icon_inactive": get_asset_path("Home.png"), "color_active": "#293547", "color_inactive": "#2F2F3A"},
    "map": {"icon_active": get_asset_path("Location_b.png"), "icon_inactive": get_asset_path("Location.png"), "color_active": "#293547", "color_inactive": "#2F2F3A"},
    "car": {"icon_active": get_asset_path("Car_b.png"), "icon_inactive": get_asset_path("Car.png"), "color_active": "#293547", "color_inactive": "#2F2F3A"},
    "all_apps": {"icon_active": get_asset_path("All_Apps_b.png"), "icon_inactive": get_asset_path("All_Apps.png"), "color_active": "#293547", "color_inactive": "#2F2F3A"}
}
