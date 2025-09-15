import time
import subprocess
import os
from lib.config import (
    PLAYER_WINDOW_NAME,
    PLAYER_WINDOW_SLEEP_FOR_POSITION,
    AbbError
    )


def player_visualizer_compose(pwc_type):
    """Función para posicionar y redimensionar la ventana del visualizador/reproductor."""
    ww, wh = get_screen_resolution()
    def half_right(): return ww//2, 0, ww//2, wh
    def half_left(): return 0, 0, ww//2, wh
    def half_top(): return 0, 0, ww, wh//2
    def half_bottom(): return 0, wh//2, ww, wh//2
    def quarter_top_right(): return ww//2, 0, ww//2, wh//2
    def quarter_top_left(): return 0, 0, ww//2, wh//2
    def quarter_bottom_right(): return ww//2, wh//2, ww//2, wh//2
    def quarter_bottom_left(): return 0, wh//2, ww//2, wh//2
    values = {
        'HalfRight': half_right,
        'HalfLeft': half_left,
        'HalfTop': half_top,
        'HalfBottom': half_bottom,
        'QuarterTopRight': quarter_top_right,
        'QuarterTopLeft': quarter_top_left,
        'QuarterBottomRight': quarter_bottom_right,
        'QuarterBottomLeft': quarter_bottom_left,
    }
    x, y, w, h = values[pwc_type]()
    try:
        set_position_window(PLAYER_WINDOW_NAME, x, y, w, h)
    except subprocess.CalledProcessError as e:
        raise AbbError(f"ERROR al posicionar la ventana.")


def set_position_window(window_title, x, y, width, height):
    """Función para posicionar y redimensionar la ventana del visualizador/reproductor."""
    time.sleep(PLAYER_WINDOW_SLEEP_FOR_POSITION)
    subprocess.run(
        ["wmctrl", "-r", window_title, "-e",
         f"0,{x},{y},{width},{height}"],
        check=True)


def get_screen_resolution():
    """Función para obtener dimensiones de pantalla"""
    result = subprocess.run(
        ["xrandr", "--current"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
        )
    # Busca la línea con la resolución actual
    for line in result.stdout.splitlines():
        if "*" in line:
            resolution = line.split()[0]
            width, height = map(int, resolution.split("x"))
            return width, height


def get_activewindow_id():
    """Función que obtiene el id de la ventana activa. Para Linux."""
    try:
        p = subprocess.run(
            ["xdotool", "getwindowfocus"],
            capture_output=True,
            text=True
        )
        return p.stdout.strip()
    except Exception as e:
        raise AbbError(f"ERROR al obtener el título de la ventana: {e}")


def clear_screen():
    """Función para limpiar la consola."""
    os.system('clear')


def focus_window(window_id):
    """Función para poner en foco alguna ventana específica."""
    subprocess.run(["xdotool", "windowactivate", window_id])
