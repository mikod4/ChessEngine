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
        
    def reset_board(self):
        self.board.reset()

    def get_last_move(self):
        if self.board.move_stack:
            move = self.board.peek()
            self.board.pop()

            last_move = self.board.san(move)
            self.board.push(move)

            return last_move
        
        return None

    def get_check_square(self):
        if self.board.is_check():
            return chess.square_name(self.board.king(self.board.turn))
        return None

    def is_game_over(self):
        return self.board.is_game_over() or self.board.can_claim_threefold_repetition()
    
    def get_game_result(self):
        if self.board.is_checkmate():
            return "checkmate"
        elif self.board.is_stalemate():
            return "stalemate"
        elif self.board.is_insufficient_material():
            return "insufficient_material"
        elif self.board.is_seventyfive_moves():
            return "seventyfive_moves"
        elif self.board.can_claim_threefold_repetition():
            return "threefold_repetition"
        else:
            return "ongoing"
        
    def get_turn(self):
        return "white" if self.board.turn == chess.WHITE else "black"
    
    def promote_pawn(self, move_uci, promotion_piece, color):
        try:
            move = chess.Move.from_uci(move_uci)
            if move in self.board.legal_moves:
                move.promotion = promotion_piece
                self.board.push(move)
                return True
            else:
                return False
        except ValueError:
            return False
        
    def get_board_fen(self):
        return self.board.fen()
    
    def set_board_fen(self, fen):
        self.board.set_fen(fen)
