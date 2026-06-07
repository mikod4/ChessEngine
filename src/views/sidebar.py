from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView
from src.utils.constants import TABLE_COLUMNS

class Sidebar(QWidget):
    def __init__(self):
        super().__init__()

        self.last_col = 0
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        self.move_table = QTableWidget()
        self.move_table.setRowCount(0)
        self.move_table.setColumnCount(2)
        self.move_table.setHorizontalHeaderLabels(TABLE_COLUMNS)

        self.move_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        layout.addWidget(self.move_table)

    def add_move(self, move_str):
        if self.last_col == 0:
            self.move_table.insertRow(self.move_table.rowCount())
        
        self.move_table.setItem(self.move_table.rowCount() - 1, self.last_col, QTableWidgetItem(move_str))
        self.last_col = (self.last_col + 1) % 2
        self.move_table.scrollToBottom()

    def toggle_side_bar(self, show):
        self.setVisible(show)

    def restart(self):
        self.move_table.setRowCount(0)
        self.last_col = 0
