from PyQt6.QtCore import QObject, pyqtSignal
from src.engine import chess_model



class GameController(QObject):
    board_updated = pyqtSignal(str)
    illegal_move = pyqtSignal()
    show_highlights = pyqtSignal(list)
    clear_highlights = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.model = chess_model.ChessModel()
        self.selected_square = None


    def make_move(self, move_uci):
        if self.model.try_move(move_uci):
            self.board_updated.emit(self.model.get_board_fen())
        else:
            self.illegal_move.emit()

    def handle_square_click(self, square):
        if self.selected_square:
            move_str = f"{self.selected_square}{square}"

            if self.model.try_move(move_str):
                self.selected_square = None
                self.clear_highlights.emit()
                self.board_updated.emit(self.model.get_board_fen())
            elif self.selected_square == square:
                self.selected_square = None
                self.clear_highlights.emit()
            else:
                self.selected_square = square
                legal_moves = self.model.get_legal_moves(square)
                self.clear_highlights.emit()
                self.show_highlights.emit(legal_moves)
        else:
            self.selected_square = square
            legal_moves = self.model.get_legal_moves(square)
            self.show_highlights.emit(legal_moves)