import chess

class ChessModel:
    def __init__(self):
        self.board = chess.Board()

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