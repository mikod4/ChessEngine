import pytest
import chess
from src.engine.bots.bot_minimax import MinimaxBot


@pytest.fixture
def bot():
    return MinimaxBot(depth=2)

def test_evaluate_initial_board_is_zero(bot):
    board = chess.Board()
    evaluation = bot.evaluate_board(board)
    assert evaluation == 0, "Ocena pozycji początkowej powinna wynosić 0"

def test_finds_mate_in_one_for_white(bot):
    # m1
    board = chess.Board("r1bqk1nr/pppp1ppp/2n5/2b1p3/2B1P3/5Q2/PPPP1PPP/RNB1K1NR w KQkq - 4 4")
    best_move = bot.get_move(board)
    assert best_move == "f3f7", "Bot powinien znaleźć mata w 1"

def test_finds_mate_in_one_for_black(bot):
    # m1
    board = chess.Board("rnbqkbnr/pppp1ppp/8/4p3/5PP1/8/PPPPP2P/RNBQKBNR b KQkq g3 0 2")
    best_move = bot.get_move(board)
    assert best_move == "d8h4", "Bot powinien znaleźć mata w 1"

def test_captures_hanging_piece(bot):
    # darmowe bicie hetmana
    board = chess.Board("r1b1k2r/pppp1ppp/5n2/3Q4/4P3/8/PPP2PPP/RNB1KB1R b KQkq - 0 1")
    best_move = bot.get_move(board)
    assert best_move == "f6d5", "Czarny bot powinien zbić darmowego hetmana na d5"

def test_avoids_obvious_blunder(bot):
    # ucieczka wieżą
    board = chess.Board("b3k3/8/8/8/8/8/8/R3K3 w Q - 0 1")
    best_move = bot.get_move(board)
    assert best_move.startswith("a1"), "Biały bot powinien uciec atakowaną wieżą z a1"

# def test_pawn_promotion(bot):
#     board = chess.Board("4k3/3P4/8/8/8/8/8/4K3 w - - 0 1")
#     best_move = bot.get_move(board)
#     assert best_move == "d7d8q", "Bot powinien promować piona na hetmana"

def test_order_moves_prioritizes_captures(bot):
    board = chess.Board("rnbqkbnr/ppp1pppp/8/3p4/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2")
    ordered_moves = bot.order_moves(board)
    
    first_move = ordered_moves[0]
    assert board.is_capture(first_move), "Bicia powinny znajdować się na początku posortowanej listy ruchów"