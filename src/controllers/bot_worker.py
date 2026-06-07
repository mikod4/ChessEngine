from PyQt6 import QThread, pyqtSignal

class BotWorker(QThread):
    move_ready = pyqtSignal(str)

    def __init__(self, fen_state):
        super().__init__()
        self.fen_state = fen_state

    def run(self):
        pass