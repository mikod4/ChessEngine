from PyQt6.QtCore import QObject, pyqtSignal
import chess
from src.engine import chess_model
from src.utils.constants import FEN_DEFAULT
from src.controllers.bot_worker import BotWorker


class GameController(QObject):
    board_updated = pyqtSignal(str)
    move_made = pyqtSignal(str)
    eval_ready = pyqtSignal(float)
    illegal_move = pyqtSignal()
    show_move_highlights = pyqtSignal(list)
    clear_move_highlights = pyqtSignal()
    highlight_check = pyqtSignal(str)
    clear_check_highlight = pyqtSignal()
    highlight_last_move = pyqtSignal(str, str)
    clear_last_move_highlight = pyqtSignal()
    promote_pawn = pyqtSignal(str, str)


    def __init__(self):
        super().__init__()
        self.model = chess_model.ChessModel(FEN_DEFAULT)
        self.player_color = chess.WHITE
        self.selected_square = None

        self.bot_strategy = None
        self.is_bot_enabled = False
        self.is_bot_thinking = False
        self.bot_thread = None

    def run_initial_checks(self):
        if self.model.get_check_square():
            self.highlight_check.emit(self.model.get_check_square())

    def make_move(self, move_uci):
        move_str = str(move_uci)

        if self.model.try_move(move_uci):
            self.board_updated.emit(self.model.get_board_fen())

            last_move = self.model.get_last_move()
            self.move_made.emit(last_move)

            if move_str and len(move_str) >= 4:
                start_square = move_str[:2]
                end_square = move_str[2:4]
                self.highlight_last_move.emit(start_square, end_square)

            if self.model.get_check_square():
                self.highlight_check.emit(self.model.get_check_square())
            else:
                self.clear_check_highlight.emit()


            if self.is_bot_enabled and not self.is_bot_thinking:
                if self.is_bot_turn():
                    self.trigger_bot_turn()

            return True

        else:
            self.illegal_move.emit()
            return False
        
    def set_player_color(self, is_white):
        self.player_color = chess.WHITE if is_white else chess.BLACK

        if self.is_bot_enabled and not self.is_bot_thinking:
            if self.is_bot_turn():
                self.trigger_bot_turn()

    def set_bot_strategy(self, strategy):
        self.bot_strategy = strategy

    def set_bot_enabled(self, enabled):
        self.is_bot_enabled = enabled
        if enabled and not self.is_bot_thinking and self.is_bot_turn():
            self.trigger_bot_turn()

    def is_bot_turn(self):
        current_turn = self.model.get_turn()
        return (current_turn == "white" and self.player_color == chess.BLACK) or \
               (current_turn == "black" and self.player_color == chess.WHITE)

    def trigger_bot_turn(self):
        self.is_bot_thinking = True
        
        self.bot_thread = BotWorker(self.model.get_board_fen(), self.bot_strategy)
        
        self.bot_thread.move_ready.connect(self.on_bot_move_ready)
        self.bot_thread.eval_ready.connect(self.eval_ready.emit)
        self.bot_thread.finished.connect(self.bot_thread.deleteLater)

        self.bot_thread.start()

    def on_bot_move_ready(self, move_uci):
        self.is_bot_thinking = False
        if self.is_bot_enabled and self.is_bot_turn():
            self.make_move(move_uci)
            
    def get_board_fen(self):
        return self.model.get_board_fen()
    
    def restart_game(self):
        self.model = chess_model.ChessModel(FEN_DEFAULT)
        self.board_updated.emit(self.model.get_board_fen())
        self.selected_square = None
        self.clear_move_highlights.emit()
        self.clear_check_highlight.emit()
        self.clear_last_move_highlight.emit()

        if self.is_bot_enabled and self.is_bot_turn():
            self.trigger_bot_turn()

    def handle_square_click(self, square):
        if self.is_bot_thinking:
            return
        
        if self.is_bot_enabled and self.is_bot_turn():
            return

        if self.selected_square:
            move_str = f"{self.selected_square}{square}"
            
            if self.selected_square == square:
                self.selected_square = None
                self.clear_move_highlights.emit()
                return

            if self.is_promotion_move(self.selected_square, square):
                self.promote_pawn.emit(self.selected_square, square)
                self.selected_square = None
                self.clear_move_highlights.emit()
                return

            if self.make_move(move_str):
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

    def is_promotion_move(self, from_sq, to_sq) -> bool:
        piece = self.model.board.piece_at(chess.parse_square(from_sq))
        if piece and piece.piece_type == chess.PAWN:
            to_rank = to_sq[1]
            if (piece.color == chess.WHITE and to_rank == '8') or \
               (piece.color == chess.BLACK and to_rank == '1'):
                try_move = f"{from_sq}{to_sq}q"
                return chess.Move.from_uci(try_move) in self.model.board.legal_moves
        return False

    def complete_pawn_promotion(self, from_sq, to_sq, piece_char):
        move_uci = f"{from_sq}{to_sq}{piece_char}"
        self.make_move(move_uci)


    def load_game_from_fen(self, fen):
        self.model = chess_model.ChessModel(fen)
        self.board_updated.emit(fen)
        self.selected_square = None
        self.clear_move_highlights.emit()
        self.clear_check_highlight.emit()
        self.clear_last_move_highlight.emit()
