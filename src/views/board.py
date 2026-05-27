from weakref import ref

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPainter, QColor, QBrush
from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsEllipseItem
from PyQt6.QtSvgWidgets import QGraphicsSvgItem

SQUARE_SIZE = 60
COLOR = [(240, 217, 181), (181, 136, 99)]
HIGLIGHT_COLOR = QColor(255, 70, 70, 80)
CHECK_COLOR = QColor(255, 0, 0, 150)

class Board(QGraphicsView):
    square_clicked = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)

        self.setFixedSize(SQUARE_SIZE * 8, SQUARE_SIZE * 8)
        self.scene = QGraphicsScene(self)
        
        self.scene.setSceneRect(0, 0, SQUARE_SIZE * 8, SQUARE_SIZE * 8)
        self.setScene(self.scene)

        self.hint_items = []

        self.draw_board()

    def draw_board(self):
        colors = [QColor(*x) for x in COLOR]
        for row in range(8):
            for col in range(8):
                color = colors[(row + col) % 2]
                rect = QGraphicsRectItem(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                rect.setBrush(QBrush(color))
                self.scene.addItem(rect)

    def clear_check_highlight(self):
        for item in self.scene.items():
            if isinstance(item, QGraphicsRectItem) and item.brush().color() == CHECK_COLOR:
                self.scene.removeItem(item)
    
    def highlight_check(self, square):
        col = ord(square[0]) - ord('a')
        row = 8 - int(square[1])

        rect = QGraphicsRectItem(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
        rect.setBrush(QBrush(CHECK_COLOR))
        rect.setZValue(4)
        self.scene.addItem(rect)

    def clear_move_highlights(self):
        for dot in self.hint_items:
            self.scene.removeItem(dot)
        self.hint_items.clear()
    
    def show_move_highlights(self, squares):
        for sq in squares:
            col = ord(sq[2]) - ord('a')
            row = 8 - int(sq[3])

            center_x = col * SQUARE_SIZE + (SQUARE_SIZE / 2)
            center_y = row * SQUARE_SIZE + (SQUARE_SIZE / 2)

            radius = SQUARE_SIZE * 0.15

            dot = QGraphicsEllipseItem(center_x - radius, center_y - radius, radius * 2, radius * 2)

            dot.setBrush(QBrush(HIGLIGHT_COLOR))
            #dot.setPen(Qt.PenStyle.NoPen)
            dot.setZValue(5)
            
            self.scene.addItem(dot)
            self.hint_items.append(dot)
            
    
    def get_square_from_position(self, pos):
        col = int(pos.x() // SQUARE_SIZE)
        row = int(pos.y() // SQUARE_SIZE)

        if 0 <= col < 8 and 0 <= row < 8:
           return f"{chr(col + ord('a'))}{8 - row}"
        return None
    
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            pos = self.mapToScene(event.pos())
            square = self.get_square_from_position(pos)
            if square:
                self.square_clicked.emit(square)

        super().mousePressEvent(event)
        
        

    def update_board(self, fen):
        for item in self.scene.items():
            if isinstance(item, QGraphicsSvgItem):
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