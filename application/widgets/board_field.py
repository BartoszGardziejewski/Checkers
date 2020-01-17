from enum import Enum

from PyQt5.QtCore import QSize, pyqtSlot
from PyQt5.QtWidgets import QPushButton


class Pawn(Enum):
    Empty = 0,
    White = 1,
    Black = 2,


class BoardField(QPushButton):
    def __init__(self, row, column):
        super().__init__()
        size = 50
        self.setFixedSize(QSize(size, size))
        self.callback = lambda field: print("Error: BoardField.callback NOT DEFINED")
        self.clicked.connect(self.on_click)
        self.row = row
        self.column = column
        self.pawn = Pawn.Empty
        self.set_fields_style()

    def set_fields_style(self):
        row_parity = (self.row % 2) == 0
        column_parity = (self.column % 2) == 0
        if (column_parity and not row_parity) or (row_parity and not column_parity):
            self.setStyleSheet(self.styleSheet() + ";background-color: grey")
        else:
            self.setStyleSheet(self.styleSheet() + ";background-color: cornsilk")
        self.setStyleSheet(self.styleSheet() + ";font-size: 30px")

    def activate(self):
        self.setStyleSheet(self.styleSheet() + ";border: 3px dashed blue;")

    def deactivate(self):
        self.setStyleSheet(self.styleSheet() + ";border: none")

    def mark_as_possible(self):
        self.setStyleSheet(self.styleSheet() + ";border: 3px dashed green;")

    def mark_as_mandatory(self):
        self.setStyleSheet(self.styleSheet() + ";border: 3px dashed red;")

    def put_pawn(self, pawn):
        self.setText('O')
        if pawn == Pawn.Black:
            self.setStyleSheet(self.styleSheet() + ";color: black")
        elif pawn == Pawn.White:
            self.setStyleSheet(self.styleSheet() + ";color: white")
        self.pawn = pawn

    def remove_pawn(self):
        self.setText('')
        self.pawn = Pawn.Empty

    def set_clicked_callback(self, callback):
        self.callback = callback

    @pyqtSlot(name="on_click")
    def on_click(self):
        self.callback(self)
