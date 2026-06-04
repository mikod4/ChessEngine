from PyQt6.QtCore import QObject, pyqtSignal, QThread
import subprocess
import chess
from src.engine import chess_model
from src.engine.bots import bot_random
from src.utils.constants import FEN_DEFAULT


class GameController(QObject):
    board_updated = pyqtSignal(str)
    move_made = pyqtSignal(str)
    illegal_move = pyqtSignal()
    show_move_highlights = pyqtSignal(list)
    clear_move_highlights = pyqtSignal()
    highlight_check = pyqtSignal(str)
    clear_check_highlight = pyqtSignal()
    game_over = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.model = chess_model.ChessModel(FEN_DEFAULT)
        self.bot_model = bot_random.RandomBot()
        self.player_color = chess.WHITE
        self.selected_square = None

    def run_initial_checks(self):
        if self.model.get_check_square():
            self.highlight_check.emit(self.model.get_check_square())

    def make_move(self, move_uci):
        if self.model.try_move(move_uci):
            self.board_updated.emit(self.model.get_board_fen())
            self.move_made.emit(self.model.get_last_move())

            if self.model.get_check_square():
                self.highlight_check.emit(self.model.get_check_square())
            else:
                self.clear_check_highlight.emit()

            if not self.model.is_game_over() and self.model.board.turn != self.player_color:

                subprocess.call(self.make_bot_move())

            return True

        else:
            self.illegal_move.emit()
            return False

    def make_bot_move(self):
        self.make_move(
            self.bot_model.get_move(
                self.model.get_board()
            )
        )

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
