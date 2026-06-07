from PyQt6.QtGui import QColor

# MainWindow
TITLE = "Chess"
ICON_PATH = "assets/icons/icon.svg"
SIDEBAR_SIZE = 280

# Board
SQUARE_SIZE = 60
COLOR = [(240, 217, 181), (181, 136, 99)]
HIGLIGHT_COLOR = QColor(255, 70, 70, 80)
CHECK_COLOR = QColor(255, 0, 0, 150)

# EvalutaionBar
START_EVAL = 50
FORMAT_EVAL = "0.0"
MIN_EVAL = -5.0
MAX_EVAL = 5.0

# Sidebar
TABLE_COLUMNS = ["Białe", "Czarne"]

# Pieces
PIECES_ICONS = "assets/images/pieces/"

# Sounds
CAPTURE_SOUND = "assets/sounds/capture.wav"
CASTLE_SOUND = "assets/sounds/castle.wav"
CHECK_SOUND = "assets/sounds/check.wav"
MOVE_SOUND = "assets/sounds/move.wav"
ILLEGAL_SOUND = "assets/sounds/illegal.wav"



# FEN
FEN_DEFAULT = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
FEN_TEST_1 = "r1bqkbnr/pppp1ppp/2n5/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 2 3"
FEN_TEST_2 = "r1bqkbnr/pppppppp/8/2n5/4K3/8/PPPPPPPP/RNBQ1BNR w KQkq - 0 1"
