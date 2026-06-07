import chess
from src.engine.bots.bot_template import Bot
from src.utils.constants import MINIMAX_DEPTH

class MinimaxBot(Bot):
    def __init__(self, depth=MINIMAX_DEPTH):
        super().__init__()
        self.depth = depth

        self.piece_values = {
            chess.PAWN: 100,
            chess.KNIGHT: 300,
            chess.BISHOP: 300,
            chess.ROOK: 500,
            chess.QUEEN: 900,
            chess.KING: 9000
        }

    def get_move(self, board) -> str:
        best_move = None
        is_white = board.turn == chess.WHITE
        alpha = -float('inf')
        beta = float('inf')
        best_eval = float('-inf') if board.turn else float('inf')

        for move in self.order_moves(board):
            board.push(move)
            eval = self.minimax(board, self.depth - 1, alpha, beta, not is_white)
            board.pop()


            if is_white:
                if eval > best_eval:
                    best_eval = eval
                    best_move = move
                alpha = max(alpha, eval)
            elif not is_white:
                if eval < best_eval:
                    best_eval = eval
                    best_move = move
                beta = min(beta, eval)
            
        return best_move.uci() if best_move else list(board.legal_moves)[0].uci()
    

    def minimax(self, board, depth, alpha, beta, is_maximizing_white):
        if depth == 0 or board.is_game_over():
            return self.evaluate_board(board)

        if is_maximizing_white:
            max_eval = -float('inf')
            
            for move in self.order_moves(board):
                board.push(move)
                eval = self.minimax(board, depth - 1, alpha, beta, False)
                board.pop()
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)

                if beta <= alpha:
                    break

            return max_eval
        else:
            min_eval = float('inf')
            
            for move in self.order_moves(board):
                board.push(move)
                eval = self.minimax(board, depth - 1, alpha, beta, True)
                board.pop()
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)

                if beta <= alpha:
                    break

            return min_eval
        
    def evaluate_board(self, board):
        if board.is_checkmate():
            return float('inf') if board.turn == chess.BLACK else float('-inf')
        
        eval = 0
        for piece_type in self.piece_values:
            white_pieces = board.pieces(piece_type, chess.WHITE)
            black_pieces = board.pieces(piece_type, chess.BLACK)

            eval += len(white_pieces) * self.piece_values[piece_type]
            eval -= len(black_pieces) * self.piece_values[piece_type]

            center_squares = chess.SquareSet(chess.BB_CENTER)
            eval += len(white_pieces & center_squares) * 15
            eval -= len(black_pieces & center_squares) * 15

            if piece_type == chess.PAWN:
                for sq in white_pieces:
                    eval += chess.square_rank(sq) * 10
                for sq in black_pieces:
                    eval -= (7 - chess.square_rank(sq)) * 10

        return eval
    
    def order_moves(self, board):
        moves = list(board.legal_moves)
        moves.sort(key=lambda move: board.is_capture(move), reverse=True)
        return moves
