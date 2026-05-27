from PyQt6.QtCore import QObject, pyqtSignal
from src.engine import chess_model



class GameController(QObject):
    board_updated = pyqtSignal(str)
    illegal_move = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.model = chess_model.ChessModel()

    def make_move(self, move_uci):
        if self.model.try_move(move_uci):
            self.board_updated.emit(self.model.get_board_fen())
        else:
            self.illegal_move.emit()