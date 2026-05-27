from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QAction, QActionGroup
from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QLayout
from src.controllers.game_controller import GameController
from src.views.board import Board
from src.views.sidebar import Sidebar
from src.views.evaluation_bar import EvaluationBar
from src.utils.constants import TITLE, ICON_PATH, SIDEBAR_SIZE



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(TITLE)
        self.setWindowIcon(QIcon(ICON_PATH))

        self.controller = GameController()

        self.setup_ui()
        self.update_board()

        self.board.square_clicked.connect(self.controller.handle_square_click)
        self.controller.board_updated.connect(self.board.update_board)

        self.controller.move_made.connect(self.sidebar.add_move)

        self.controller.show_move_highlights.connect(self.board.show_move_highlights)
        self.controller.clear_move_highlights.connect(self.board.clear_move_highlights)
        self.controller.illegal_move.connect(self.play_error_sounds)
        self.controller.highlight_check.connect(self.board.highlight_check)
        self.controller.clear_check_highlight.connect(self.board.clear_check_highlight)

        self.controller.run_initial_checks()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QHBoxLayout(central_widget)

        layout.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)

        self.eval_bar = EvaluationBar()
        self.board = Board()
        self.sidebar = Sidebar()

        self.sidebar.setFixedWidth(SIDEBAR_SIZE)

        layout.addWidget(self.eval_bar)
        layout.addWidget(self.board)
        layout.addWidget(self.sidebar)

        self.layout().setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)

        self.create_menu()


    def create_menu(self):
        menu_bar = self.menuBar()

        self.view_menu = menu_bar.addMenu("Pokaż")

        self.toggle_eval_action = QAction("Pasek Ewaluacji", self)
        self.toggle_eval_action.setCheckable(True)
        self.toggle_eval_action.setChecked(True) 
        self.toggle_eval_action.triggered.connect(self.eval_bar.toggle_eval_bar)
        self.view_menu.addAction(self.toggle_eval_action)

        self.view_menu.addSeparator()

        self.toggle_sidebar_action = QAction("Ruchy", self)
        self.toggle_sidebar_action.setCheckable(True)
        self.toggle_sidebar_action.setChecked(True)
        self.toggle_sidebar_action.triggered.connect(self.sidebar.toggle_side_bar)
        self.view_menu.addAction(self.toggle_sidebar_action)

        
        
        self.bot_menu = menu_bar.addMenu("Silnik")
        
        self.engine_group = QActionGroup(self)
        self.engine_group.setExclusive(True)


        self.engine1_action = QAction("Włącz Silnik 1", self)
        self.engine1_action.setCheckable(True)
        self.engine1_action.setChecked(True)
        self.engine_group.addAction(self.engine1_action)
        self.bot_menu.addAction(self.engine1_action)

        self.bot_menu.addSeparator()

        self.engine2_action = QAction("Włącz Silnik 2", self)
        self.engine2_action.setCheckable(True)
        self.engine_group.addAction(self.engine2_action)
        self.bot_menu.addAction(self.engine2_action)

        self.engine_group.triggered.connect(self.change_bot)

    def change_bot(self, engine):
        print(f"Changing bot to: {engine.text()}")

        if engine == self.engine1_action:
            pass
        elif engine == self.engine2_action:
            pass

    def update_board(self):
        self.board.update_board(self.controller.model.get_board_fen())

    def play_error_sounds(self):
        print("Illegal move attempted!")