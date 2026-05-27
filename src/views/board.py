from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QColor, QBrush, QPixmap, QImage
from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsPixmapItem
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtSvgWidgets import QGraphicsSvgItem

SQUARE_SIZE = 60
COLOR = [(240, 217, 181), (181, 136, 99)]
BORDER_OFFSET = 5

class Board(QGraphicsView):
    def __init__(self):
        super().__init__()

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)

        self.setFixedSize(SQUARE_SIZE * 8 + BORDER_OFFSET, SQUARE_SIZE * 8 + BORDER_OFFSET)
        self.scene = QGraphicsScene(self)
        
        self.scene.setSceneRect(0, 0, SQUARE_SIZE * 8, SQUARE_SIZE * 8)
        self.setScene(self.scene)

        self.draw_board()

    def draw_board(self):
        colors = [QColor(*x) for x in COLOR]
        for row in range(8):
            for col in range(8):
                color = colors[(row + col) % 2]
                rect = QGraphicsRectItem(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                rect.setBrush(QBrush(color))
                self.scene.addItem(rect)

    def update_board(self, fen):
        for item in self.scene.items():
            if isinstance(item, QGraphicsPixmapItem):
                self.scene.removeItem(item)

        rows = fen.split()[0].split('/')
        for row_index, row in enumerate(rows):
            col_index = 0
            for char in row:
                if char.isdigit():
                    col_index += int(char)
                else:
                    piece_item = QGraphicsSvgItem(f"assets/images/pieces/{char}.svg")
                    bounds = piece_item.boundingRect()
                    scale = SQUARE_SIZE / max(bounds.width(), bounds.height())
                    piece_item.setScale(scale)
                    piece_item.setPos(col_index * SQUARE_SIZE, row_index * SQUARE_SIZE)
                    self.scene.addItem(piece_item)
                    col_index += 1