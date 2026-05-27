from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QProgressBar, QListWidget
from src.controllers.game_controller import GameController
from src.views.board import Board

START = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Chess")
        self.setWindowIcon(QIcon("assets/icons/icon.svg"))

        self.controller = GameController()

        self.controller.board_updated.connect(self.update_board)
        self.controller.illegal_move.connect(self.play_error_sounds)

        self.setup_ui()
        self.update_board(START)
        #self.toggle_eval_bar()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QHBoxLayout(central_widget)

        self.eval_bar = QProgressBar()
        self.eval_bar.setOrientation(Qt.Orientation.Vertical)
        self.eval_bar.setValue(50)
        #self.eval_bar.setFixedWidth(30)

        self.board_view = Board()

        self.pgn_list = QListWidget()
        #self.pgn_list.setFixedWidth(200) 

        layout.addWidget(self.eval_bar)
        layout.addWidget(self.board_view)
        layout.addWidget(self.pgn_list)
    
    def toggle_eval_bar(self, show=None):
        if show is None:
            show = not self.eval_bar.isVisibleTo(self)
        self.eval_bar.setVisible(show)

    def update_board(self, fen):
        self.board_view.update_board(fen)

    def play_error_sounds(self):
        print("Illegal move attempted!")