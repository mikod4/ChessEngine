from PyQt6.QtGui import QColor
import sys
import os

def get_asset_path(relative_path):
    """ Get absolute path to resource, necessary for pyinstaller to work """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# MainWindow
TITLE = "Chess"
ICON_PATH = get_asset_path("assets/icons/icon.svg")
SIDEBAR_SIZE = 280

# Bot settings
MINIMAX_DEPTH = 3

# Board
SQUARE_SIZE = 60
COLOR = [(240, 217, 181), (181, 136, 99)]
HIGLIGHT_COLOR = QColor(255, 70, 70, 80)
CHECK_COLOR = QColor(255, 0, 0, 150)
LAST_MOVE_COLOR = QColor(155, 199, 0, 100)

# EvalutaionBar
START_EVAL = 50
FORMAT_EVAL = "0.0"
MIN_EVAL = -5.0
MAX_EVAL = 5.0

# Sidebar
TABLE_COLUMNS = ["Białe", "Czarne"]

# Pieces
PIECES_ICONS = get_asset_path("assets/images/pieces/")

# Sounds
CAPTURE_SOUND = get_asset_path("assets/sounds/capture.wav")
CASTLE_SOUND = get_asset_path("assets/sounds/castle.wav")
CHECK_SOUND = get_asset_path("assets/sounds/check.wav")
MOVE_SOUND = get_asset_path("assets/sounds/move.wav")
ILLEGAL_SOUND = get_asset_path("assets/sounds/illegal.wav")

# FEN
FEN_DEFAULT = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
FEN_TEST_1 = "r1bqkbnr/pppp1ppp/2n5/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 2 3"
FEN_TEST_2 = "r1bqkbnr/pppppppp/8/2n5/4K3/8/PPPPPPPP/RNBQ1BNR w KQkq - 0 1"
