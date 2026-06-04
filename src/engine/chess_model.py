import chess


class ChessModel:
    def __init__(self, fen=None):
        self.board = chess.Board(fen) if fen else chess.Board()

    def try_move(self, move_uci):
        try:
            move = chess.Move.from_uci(move_uci)
            if move in self.board.legal_moves:
                self.board.push(move)
                return True
            else:
                return False
        except ValueError:
            return False

    def get_legal_moves(self, square):
        try:
            square_index = chess.parse_square(square)
            return [move.uci() for move in self.board.legal_moves if move.from_square == square_index]
        except ValueError:
            return []

    def get_board_fen(self):
        return self.board.fen()

    def get_board(self):
        return self.board

    def get_check_square(self):
        if self.board.is_check():
            return chess.square_name(self.board.king(self.board.turn))
        return None

    def is_game_over(self):
        return self.board.is_game_over()

    def get_last_move(self):
        if self.board.move_stack:
            move = self.board.peek()
            self.board.pop()

            last_move = self.board.san(move)
            self.board.push(move)

            return last_move

        return None
