from PyQt6.QtCore import QThread, pyqtSignal
import chess

class BotWorker(QThread):
    move_ready = pyqtSignal(str)

    def __init__(self, fen_state, bot_strategy):
        super().__init__()
        self.fen_state = fen_state
        self.bot_strategy = bot_strategy

    def run(self):
        board_copy = chess.Board(self.fen_state)
        move_uci = self.bot_strategy.get_move(board_copy)
        
        self.move_ready.emit(move_uci)