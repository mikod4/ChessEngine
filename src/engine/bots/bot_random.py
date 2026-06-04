from time import sleep
from src.engine.bots.bot_template import Bot
from random import choice
import chess


class RandomBot(Bot):
    def get_move(self, board: chess.Board) -> str:
        legal_moves = list(board.legal_moves)
        sleep(1)
        return choice(legal_moves).uci()
