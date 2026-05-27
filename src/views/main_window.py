from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QProgressBar, QTableWidget, QTableWidgetItem
from src.controllers.game_controller import GameController
from src.views.board import Board



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Chess")
        self.setWindowIcon(QIcon("assets/icons/icon.svg"))

        self.controller = GameController()

        self.setup_ui()
        self.update_board()

        self.last_col = 0

        self.board.square_clicked.connect(self.controller.handle_square_click)
        self.controller.board_updated.connect(self.board.update_board)
        self.controller.move_made.connect(self.add_move_to_pgn)
        self.controller.show_move_highlights.connect(self.board.show_move_highlights)
        self.controller.clear_move_highlights.connect(self.board.clear_move_highlights)
        self.controller.illegal_move.connect(self.play_error_sounds)
        self.controller.highlight_check.connect(self.board.highlight_check)
        self.controller.clear_check_highlight.connect(self.board.clear_check_highlight)

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QHBoxLayout(central_widget)

        self.eval_bar = QProgressBar()
        self.eval_bar.setOrientation(Qt.Orientation.Vertical)
        self.eval_bar.setValue(50)

        self.board = Board()

        self.pgn_list = QTableWidget()
        self.pgn_list.setRowCount(0)
        self.pgn_list.setColumnCount(2)
        self.pgn_list.setHorizontalHeaderLabels(["Białe", "Czarne"])

        layout.addWidget(self.eval_bar)
        layout.addWidget(self.board)
        layout.addWidget(self.pgn_list)

        self.create_menu()


    def create_menu(self):
        menu_bar = self.menuBar()

        self.view_menu = menu_bar.addMenu("Pokaż")

        self.toggle_eval_action = QAction("Pasek Ewaluacji", self)
        self.toggle_eval_action.setCheckable(True)
        self.toggle_eval_action.setChecked(True) 
        self.toggle_eval_action.triggered.connect(self.toggle_eval_bar)
        self.view_menu.addAction(self.toggle_eval_action)

        self.view_menu.addSeparator()

        self.toggle_pgn_action = QAction("Notacja PGN", self)
        self.toggle_pgn_action.setCheckable(True)
        self.toggle_pgn_action.setChecked(True)
        self.toggle_pgn_action.triggered.connect(self.toggle_pgn_list)
        self.view_menu.addAction(self.toggle_pgn_action)

        
        
        self.bot_menu = menu_bar.addMenu("Silnik")

        self.engine1_action = QAction("Włącz Silnik 1", self)
        self.engine1_action.setCheckable(True)
        self.engine1_action.setChecked(True)
        self.engine1_action.triggered.connect(lambda: self.change_bot(self.engine1_action))
        self.bot_menu.addAction(self.engine1_action)

        self.bot_menu.addSeparator()

        self.engine2_action = QAction("Włącz Silnik 2", self)
        self.engine2_action.setCheckable(True)
        self.engine2_action.triggered.connect(lambda: self.change_bot(self.engine2_action))
        self.bot_menu.addAction(self.engine2_action)


    def add_move_to_pgn(self, move):
        if self.last_col == 0:
            self.pgn_list.insertRow(self.pgn_list.rowCount())

        self.pgn_list.setItem(self.pgn_list.rowCount()-1, self.last_col, QTableWidgetItem(move))

        self.last_col = (self.last_col + 1) % 2


        self.pgn_list.scrollToBottom()

    def change_bot(self, engine_action):
        print(f"Changing bot to: {engine_action.text()}")

        for menu_item in self.bot_menu.actions():
            if menu_item != engine_action:
                menu_item.setChecked(False)

    def toggle_eval_bar(self, show=None):
        if show is None:
            show = not self.eval_bar.isVisibleTo(self)
        self.eval_bar.setVisible(show)

    def toggle_pgn_list(self, show=None):
        if show is None:
            show = not self.pgn_list.isVisibleTo(self)
        self.pgn_list.setVisible(show)

    def update_board(self):
        self.board.update_board(self.controller.model.get_board_fen())

    def play_error_sounds(self):
        print("Illegal move attempted!")