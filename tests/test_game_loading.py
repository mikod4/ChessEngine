import pytest
from unittest.mock import MagicMock
from PyQt6.QtWidgets import QFileDialog, QMessageBox, QApplication

from src.views.main_window import MainWindow


@pytest.fixture(scope="session", autouse=True)
def q_application():
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    yield app


@pytest.fixture
def window(monkeypatch):
    monkeypatch.setattr("src.views.main_window.QSoundEffect", MagicMock)
    
    win = MainWindow()
    # Izolujemy kontroler, by testować wyłącznie reakcję okna na wczytanie pozycji
    win.controller = MagicMock()
    return win


def test_load_game_success(window, monkeypatch):
    test_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    
    monkeypatch.setattr(
        QFileDialog, 
        "getOpenFileName", 
        lambda *args, **kwargs: ("saved_game.fen", "FEN Files (*.fen)")
    )
    
    monkeypatch.setattr(
        "src.views.main_window.load_game", 
        lambda filename: (True, test_fen)
    )
    
    mock_info = MagicMock()
    monkeypatch.setattr(QMessageBox, "information", mock_info)

    window.load_game()

    window.controller.load_game_from_fen.assert_called_once_with(test_fen)
    mock_info.assert_called_once()


def test_load_game_invalid_fen_or_file_error(window, monkeypatch):
    error_msg = "Niepoprawny format FEN"
    
    monkeypatch.setattr(
        QFileDialog, 
        "getOpenFileName", 
        lambda *args, **kwargs: ("bad_file.fen", "FEN Files (*.fen)")
    )
    
    monkeypatch.setattr(
        "src.views.main_window.load_game", 
        lambda filename: (False, error_msg)
    )
    
    mock_critical = MagicMock()
    monkeypatch.setattr(QMessageBox, "critical", mock_critical)

    window.load_game()

    window.controller.load_game_from_fen.assert_not_called()
    mock_critical.assert_called_once()


def test_load_game_cancelled_by_user(window, monkeypatch):
    monkeypatch.setattr(
        QFileDialog, 
        "getOpenFileName", 
        lambda *args, **kwargs: ("", "")
    )
    
    mock_info = MagicMock()
    mock_critical = MagicMock()
    monkeypatch.setattr(QMessageBox, "information", mock_info)
    monkeypatch.setattr(QMessageBox, "critical", mock_critical)
    
    mock_load_handler = MagicMock()
    monkeypatch.setattr("src.views.main_window.load_game", mock_load_handler)

    window.load_game()

    mock_load_handler.assert_not_called()
    window.controller.load_game_from_fen.assert_not_called()
    mock_info.assert_not_called()
    mock_critical.assert_not_called()


def test_save_game_success(window, monkeypatch):
    test_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    window.controller.get_board_fen.return_value = test_fen

    monkeypatch.setattr(
        QFileDialog, 
        "getSaveFileName", 
        lambda *args, **kwargs: ("my_save.fen", "FEN Files (*.fen)")
    )
    
    mock_save_handler = MagicMock(return_value=(True, ""))
    monkeypatch.setattr("src.views.main_window.save_game", mock_save_handler)
    
    mock_info = MagicMock()
    monkeypatch.setattr(QMessageBox, "information", mock_info)

    window.save_game()

    window.controller.get_board_fen.assert_called_once()
    mock_save_handler.assert_called_once_with(test_fen, "my_save.fen")
    mock_info.assert_called_once()