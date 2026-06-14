from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPainter, QColor, QBrush, QPen
from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsEllipseItem, QFrame
from src.views.piece import Piece
from src.utils.constants import SQUARE_SIZE, COLOR, HIGLIGHT_COLOR, CHECK_COLOR, LAST_MOVE_COLOR


class Board(QGraphicsView):
    square_clicked = pyqtSignal(str)
    promote_pawn = pyqtSignal(str, str)

    def __init__(self):
        super().__init__()
        self.is_flipped = False
        self.check_highlight_item = None

        self.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.setFrameShape(QFrame.Shape.NoFrame)

        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)

        self.setFixedSize(SQUARE_SIZE * 8, SQUARE_SIZE * 8)
        self.scene = QGraphicsScene(self)

        self.scene.setSceneRect(0, 0, SQUARE_SIZE * 8, SQUARE_SIZE * 8)
        self.setScene(self.scene)

        self.last_move_highlight_items = []
        self.hint_items = []
        self.draw_board()

    def draw_board(self):
        colors = [QColor(*x) for x in COLOR]

        pen = QPen(QColor(0, 0, 0))
        pen.setWidth(1)
        offset = pen.width() / 2.0
        adjusted_size = SQUARE_SIZE - pen.width()

        for row in range(8):
            for col in range(8):
                color = colors[(row + col) % 2]

                x = (col * SQUARE_SIZE) + offset
                y = (row * SQUARE_SIZE) + offset

                rect = QGraphicsRectItem(x, y, adjusted_size, adjusted_size)
                rect.setBrush(QBrush(color))
                rect.setPen(pen)

                self.scene.addItem(rect)

    def clear_last_move_highlight(self):
        for item in self.last_move_highlight_items:
            if item.scene() == self.scene: 
                self.scene.removeItem(item)
        self.last_move_highlight_items.clear()

    def highlight_last_move(self, start_square, end_square):
        self.clear_last_move_highlight()
        highlight_color = LAST_MOVE_COLOR 

        for square in (start_square, end_square):
            if not square:
                continue

            col = ord(square[0]) - ord('a')
            row = 8 - int(square[1])

            visual_row = 7 - row if self.is_flipped else row
            visual_col = 7 - col if self.is_flipped else col

            rect = QGraphicsRectItem(visual_col * SQUARE_SIZE, visual_row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            rect.setBrush(QBrush(highlight_color))
            rect.setPen(QPen(Qt.PenStyle.NoPen))
            rect.setZValue(1) 

            self.scene.addItem(rect)
            self.last_move_highlight_items.append(rect)

    def clear_check_highlight(self):
        if self.check_highlight_item in self.scene.items():
            self.scene.removeItem(self.check_highlight_item)
            self.check_highlight_item = None
    
    def highlight_check(self, square):
        col = ord(square[0]) - ord('a')
        row = 8 - int(square[1])

        visual_row = 7 - row if self.is_flipped else row
        visual_col = 7 - col if self.is_flipped else col

        rect = QGraphicsRectItem(visual_col * SQUARE_SIZE, visual_row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
        rect.setBrush(QBrush(CHECK_COLOR))
        rect.setZValue(4)

        self.check_highlight_item = rect
        self.scene.addItem(rect)

    def clear_move_highlights(self):
        for dot in self.hint_items:
            self.scene.removeItem(dot)
        self.hint_items.clear()

    def show_move_highlights(self, squares):
        for sq in squares:
            col = ord(sq[2]) - ord('a')
            row = 8 - int(sq[3])

            visual_row = 7 - row if self.is_flipped else row
            visual_col = 7 - col if self.is_flipped else col

            center_x = visual_col * SQUARE_SIZE + (SQUARE_SIZE / 2)
            center_y = visual_row * SQUARE_SIZE + (SQUARE_SIZE / 2)

            radius = SQUARE_SIZE * 0.15

            dot = QGraphicsEllipseItem(
                center_x - radius, center_y - radius, radius * 2, radius * 2)

            dot.setBrush(QBrush(HIGLIGHT_COLOR))
            dot.setZValue(5)

            self.scene.addItem(dot)
            self.hint_items.append(dot)

    def get_square_from_position(self, pos):
        col = int(pos.x() // SQUARE_SIZE)
        row = int(pos.y() // SQUARE_SIZE)

        if 0 <= col < 8 and 0 <= row < 8:
            if self.is_flipped:
                return f"{chr(7 - col + ord('a'))}{row + 1}"
            else:
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
            if isinstance(item, Piece):
                self.scene.removeItem(item)

        rows = fen.split()[0].split('/')
        for fen_row_index, row in enumerate(rows):
            fen_col_index = 0
            for char in row:
                if char.isdigit():
                    fen_col_index += int(char)
                else:
                    visual_row = 7 - fen_row_index if self.is_flipped else fen_row_index
                    visual_col = 7 - fen_col_index if self.is_flipped else fen_col_index
                    piece_item = Piece(char, visual_row, visual_col)

                    self.scene.addItem(piece_item)
                    fen_col_index += 1

    def set_flipped(self, flipped):
        self.is_flipped = flipped