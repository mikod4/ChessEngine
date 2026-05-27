from PyQt6.QtCore import QObject, pyqtSignal
from src.engine import chess_model

#START = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
START = "r1bqkbnr/pppp1ppp/2n5/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 2 3"


class GameController(QObject):
    board_updated = pyqtSignal(str)
    move_made = pyqtSignal(str)
    illegal_move = pyqtSignal()
    show_move_highlights = pyqtSignal(list)
    clear_move_highlights = pyqtSignal()
    highlight_check = pyqtSignal(str)
    clear_check_highlight = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.model = chess_model.ChessModel(START)
        self.selected_square = None


    def make_move(self, move_uci):
        if self.model.try_move(move_uci):
            self.board_updated.emit(self.model.get_board_fen())
            self.move_made.emit(self.model.get_last_move())

            if self.model.board.is_check():
                self.highlight_check.emit(self.model.get_check_square())
            else:
                self.clear_check_highlight.emit()

            return True
        else:
            self.illegal_move.emit()
            return False
        
    def get_board_fen(self):
        return self.model.get_board_fen()

    def handle_square_click(self, square):
        if self.selected_square:
            move_str = f"{self.selected_square}{square}"

            if self.make_move(move_str):
                self.selected_square = None
                self.clear_move_highlights.emit()
            elif self.selected_square == square:
                self.selected_square = None
                self.clear_move_highlights.emit()
            else:
                self.selected_square = square
                legal_moves = self.model.get_legal_moves(square)
                self.clear_move_highlights.emit()
                self.show_move_highlights.emit(legal_moves)
        else:
            self.selected_square = square
            legal_moves = self.model.get_legal_moves(square)
            self.show_move_highlights.emit(legal_moves)