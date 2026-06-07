from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QPushButton, QHBoxLayout, QApplication
import sys

class PromotionPopUp(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Promotion")
        self.setModal(True)

        layout = QVBoxLayout(self)

        button_layout = QHBoxLayout()
        layout.addLayout(button_layout)

        self.queen_button = QPushButton("Queen")
        self.rook_button = QPushButton("Rook")
        self.bishop_button = QPushButton("Bishop")
        self.knight_button = QPushButton("Knight")

        button_layout.addWidget(self.queen_button)
        button_layout.addWidget(self.rook_button)
        button_layout.addWidget(self.bishop_button)
        button_layout.addWidget(self.knight_button)

        self.queen_button.clicked.connect(lambda: self.promote('q'))
        self.rook_button.clicked.connect(lambda: self.promote('r'))
        self.bishop_button.clicked.connect(lambda: self.promote('b'))
        self.knight_button.clicked.connect(lambda: self.promote('n'))

    def promote(self, piece):
        self.selected_piece = piece
        self.accept()