from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from src.utils.constants import SQUARE_SIZE, PIECES_ICONS


class Piece(QGraphicsSvgItem):
    def __init__(self, piece_char, row, col):
        super().__init__(
            f"{PIECES_ICONS}/{"white" if piece_char.isupper() else "black"}/{piece_char}.svg")

        self.bounds = self.boundingRect()
        scale = SQUARE_SIZE / max(self.bounds.width(), self.bounds.height())
        self.setScale(scale)
        self.setPos(col * SQUARE_SIZE, row * SQUARE_SIZE)

    def rotate_piece(self, angle):
        self.setRotation(angle)