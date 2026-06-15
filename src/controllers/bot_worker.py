from PyQt6.QtCore import QThread, pyqtSignal
import chess

class BotWorker(QThread):
    move_ready = pyqtSignal(str)
    eval_ready = pyqtSignal(float)

    def __init__(self, fen_state, bot_strategy):
        super().__init__()
        self.fen_state = fen_state
        self.bot_strategy = bot_strategy

    def run(self):
        board_copy = chess.Board(self.fen_state)
        move_uci = self.bot_strategy.get_move(board_copy)

        eval_score = 0.0
        if hasattr(self.bot_strategy, 'evaluate_board'):
            eval_score = self.bot_strategy.evaluate_board(board_copy)

        self.eval_ready.emit(eval_score)
        self.move_ready.emit(move_uci)