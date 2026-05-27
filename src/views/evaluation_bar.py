from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QProgressBar
from src.utils.constants import START_EVAL, FORMAT_EVAL, MIN_EVAL, MAX_EVAL

class EvaluationBar(QProgressBar):
    def __init__(self):
        super().__init__()

        self.setOrientation(Qt.Orientation.Vertical)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setRange(0, 100)
        self.setValue(START_EVAL)
        self.setFormat(FORMAT_EVAL)

    def set_evaluation(self, evaluation):
        clamped_score = max(MIN_EVAL, min(MAX_EVAL, evaluation))

        percentage = (int(clamped_score + MAX_EVAL) * 10)
        self.setValue(percentage)


        if evaluation > 0:
            text = f"+{evaluation}.1f"
        elif evaluation < 0:
            text = f"-{evaluation}.1f"
        else:
            text = "0.0"

        self.setFormat(text)

    def toggle_eval_bar(self, checked):
        self.setVisible(checked)