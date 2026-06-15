from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QIcon, QAction, QActionGroup
from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QLayout, QFileDialog, QPushButton
from PyQt6.QtMultimedia import QSoundEffect

from src.controllers.game_controller import GameController
from src.engine.bots import bot_random, bot_minimax
from src.views.board import Board
from src.views.promotion_popup import PromotionPopUp
from src.views.sidebar import Sidebar
from src.views.evaluation_bar import EvaluationBar
from src.utils.constants import TITLE, ICON_PATH, SIDEBAR_SIZE, ILLEGAL_SOUND, MOVE_SOUND, CAPTURE_SOUND, CASTLE_SOUND, CHECK_SOUND
from src.utils.file_handler import save_game, load_game



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(TITLE)
        self.setWindowIcon(QIcon(ICON_PATH))

        self.controller = GameController()

        self.setup_ui()
        self.update_board()

        self.init_signals()
        self.init_sounds()

        self.controller.run_initial_checks()

    def init_signals(self):
        self.board.square_clicked.connect(self.controller.handle_square_click)
        self.controller.board_updated.connect(self.board.update_board)

        self.controller.move_made.connect(self.sidebar.add_move)
        self.controller.move_made.connect(self.play_move_sound)
        self.controller.promote_pawn.connect(self.show_promotion_dialog)

        self.controller.show_move_highlights.connect(self.board.show_move_highlights)
        self.controller.clear_move_highlights.connect(self.board.clear_move_highlights)
        self.controller.illegal_move.connect(self.play_error_sounds)
        self.controller.highlight_check.connect(self.board.highlight_check)
        self.controller.clear_check_highlight.connect(self.board.clear_check_highlight)
        self.controller.highlight_last_move.connect(self.board.highlight_last_move)
        self.controller.clear_last_move_highlight.connect(self.board.clear_last_move_highlight)

    def init_sounds(self):
        self.move_sound = QSoundEffect()
        self.move_sound.setSource(QUrl.fromLocalFile(MOVE_SOUND))

        self.capture_sound = QSoundEffect()
        self.capture_sound.setSource(QUrl.fromLocalFile(CAPTURE_SOUND))

        self.castle_sound = QSoundEffect()
        self.castle_sound.setSource(QUrl.fromLocalFile(CASTLE_SOUND))

        self.check_sound = QSoundEffect()
        self.check_sound.setSource(QUrl.fromLocalFile(CHECK_SOUND))

        self.illegal_move_sound = QSoundEffect()
        self.illegal_move_sound.setSource(QUrl.fromLocalFile(ILLEGAL_SOUND))

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
        # widok
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
        
        # bot
        self.bot_menu = menu_bar.addMenu("Bot")
        
        self.bot_group = QActionGroup(self)
        self.bot_group.setExclusive(True)


        self.no_bot_action = QAction("Brak bota", self)
        self.no_bot_action.setCheckable(True)
        self.no_bot_action.setChecked(True)
        self.bot_group.addAction(self.no_bot_action)
        self.bot_menu.addAction(self.no_bot_action)

        self.bot_menu.addSeparator()

        self.bot1_action = QAction("Random", self)
        self.bot1_action.setCheckable(True)
        self.bot_group.addAction(self.bot1_action)
        self.bot_menu.addAction(self.bot1_action)

        self.bot_menu.addSeparator()

        self.bot2_action = QAction("Minimax depth 3", self)
        self.bot2_action.setCheckable(True)
        self.bot_group.addAction(self.bot2_action)
        self.bot_menu.addAction(self.bot2_action)

        self.bot_menu.addSeparator()

        self.bot3_action = QAction("Minimax depth 5", self)
        self.bot3_action.setCheckable(True)
        self.bot_group.addAction(self.bot3_action)
        self.bot_menu.addAction(self.bot3_action)

        self.bot_group.triggered.connect(self.change_bot)

        # gra
        self.game_menu = menu_bar.addMenu("Gra")

        self.save_action = QAction("Zapisz", self)
        self.save_action.triggered.connect(self.save_game)
        self.game_menu.addAction(self.save_action)

        self.game_menu.addSeparator()

        self.load_action = QAction("Wczytaj", self)
        self.load_action.triggered.connect(self.load_game)
        self.game_menu.addAction(self.load_action)

        self.game_menu.addSeparator()

        self.restart_action = QAction("Restart", self)
        self.restart_action.triggered.connect(self.restart_game)
        self.game_menu.addAction(self.restart_action)

        # kolor
        self.color_menu = menu_bar.addMenu("Kolor")

        self.white_action = QAction("Białe", self)
        self.white_action.setCheckable(True)
        self.white_action.setChecked(True)
        self.color_menu.addAction(self.white_action)

        self.color_menu.addSeparator()

        self.black_action = QAction("Czarne", self)
        self.black_action.setCheckable(True)
        self.color_menu.addAction(self.black_action)

        self.color_group = QActionGroup(self)
        self.color_group.setExclusive(True)
        self.color_group.addAction(self.white_action)
        self.color_group.addAction(self.black_action)

        self.color_group.triggered.connect(self.toggle_board_color)
        

    def save_game(self):
        fen = self.controller.get_board_fen()
        success, message = save_game(fen)

        if not success:
            print(f"Error saving game: {message}")
        else:
            print("Game saved successfully.")

    def load_game(self):
        options = QFileDialog.Option.ReadOnly
        filename, _ = QFileDialog.getOpenFileName(self, "Wczytaj grę", "", "FEN Files (*.fen);;All Files (*)", options=options)

        if filename:
            success, result = load_game(filename)
            if success:
                self.controller.load_game_from_fen(result)
                print("Game loaded successfully.")
            else:
                print(f"Error loading game: {result}")

    def restart_game(self):
        self.controller.restart_game()
        self.eval_bar.restart()
        self.sidebar.restart()

    def change_bot(self, bot):
        print(f"Changing bot to: {bot.text()}")
        if bot == self.no_bot_action:
            self.controller.set_bot_enabled(False)
        elif bot == self.bot1_action:
            self.controller.set_bot_strategy(bot_random.RandomBot())
            self.controller.set_bot_enabled(True)
        elif bot == self.bot2_action:
            self.controller.set_bot_strategy(bot_minimax.MinimaxBot())
            self.controller.set_bot_enabled(True)
        elif bot == self.bot3_action:
            self.controller.set_bot_strategy(bot_minimax.MinimaxBot(depth=5))
            self.controller.set_bot_enabled(True)
        
    def toggle_board_color(self, action):
        if action == self.white_action:
            self.board.set_flipped(False)
            self.controller.set_player_color(is_white=True)
        elif action == self.black_action:
            self.board.set_flipped(True)
            self.controller.set_player_color(is_white=False)

        self.update_board()

    def update_board(self):
        self.board.update_board(self.controller.model.get_board_fen())

    def play_move_sound(self, move):
        if not move:
            return
        
        for sound in [self.move_sound, self.capture_sound, self.castle_sound, self.check_sound]:
            if sound.isPlaying():
                sound.stop()

        if '+' in move or '#' in move:
            self.check_sound.play()
        elif 'x' in move:
            self.capture_sound.play()
        elif 'O-O' in move:
            self.castle_sound.play()
        else:
            self.move_sound.play()

    def play_error_sounds(self):
        if self.illegal_move_sound.isPlaying():
            self.illegal_move_sound.stop()
        self.illegal_move_sound.play()

    def show_promotion_dialog(self, from_sq, to_sq):
        popup = PromotionPopUp(self)
        
        if popup.exec():
            chosen_piece = popup.selected_piece
            self.controller.complete_pawn_promotion(from_sq, to_sq, chosen_piece)
        else:
            self.update_board()