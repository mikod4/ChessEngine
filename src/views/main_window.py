from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QProgressBar, QListWidget
from src.controllers.game_controller import GameController
from src.views.board import Board

START = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Chess")
        self.setWindowIcon(QIcon("assets/icons/icon.svg"))


        self.setup_ui()
        self.update_board(START)

        self.controller = GameController()

        self.board.square_clicked.connect(self.controller.handle_square_click)
        self.controller.board_updated.connect(self.board.update_board)
        self.controller.show_highlights.connect(self.board.show_highlights)
        self.controller.clear_highlights.connect(self.board.clear_highlights)
        self.controller.illegal_move.connect(self.play_error_sounds)

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QHBoxLayout(central_widget)

        self.eval_bar = QProgressBar()
        self.eval_bar.setOrientation(Qt.Orientation.Vertical)
        self.eval_bar.setValue(50)

        self.board = Board()

        self.pgn_list = QListWidget()

        layout.addWidget(self.eval_bar)
        layout.addWidget(self.board)
        layout.addWidget(self.pgn_list)

        self.create_menu()


    def create_menu(self):
        menu_bar = self.menuBar()

        view_menu = menu_bar.addMenu("Pokaż")

        self.toggle_eval_action = QAction("Pasek Ewaluacji", self)
        self.toggle_eval_action.setCheckable(True)
        self.toggle_eval_action.setChecked(True) 
        self.toggle_eval_action.triggered.connect(self.toggle_eval_bar)
        view_menu.addAction(self.toggle_eval_action)

        view_menu.addSeparator()

        self.toggle_pgn_action = QAction("Notacja PGN", self)
        self.toggle_pgn_action.setCheckable(True)
        self.toggle_pgn_action.setChecked(True)
        self.toggle_pgn_action.triggered.connect(self.toggle_pgn_list)
        view_menu.addAction(self.toggle_pgn_action)

        bot_menu = menu_bar.addMenu("Silnik")
    
    def toggle_eval_bar(self, show=None):
        if show is None:
            show = not self.eval_bar.isVisibleTo(self)
        self.eval_bar.setVisible(show)

    def toggle_pgn_list(self, show=None):
        if show is None:
            show = not self.pgn_list.isVisibleTo(self)
        self.pgn_list.setVisible(show)

    def update_board(self, fen):
        self.board.update_board(fen)

    def play_error_sounds(self):
        print("Illegal move attempted!")