from enum import Enum

from PyQt5.QtCore import QSize, pyqtSlot
from PyQt5.QtWidgets import QPushButton


class Pawn(Enum):
    Empty = 0,
    Black = 1,
    White = 2


class BoardField(QPushButton):
    def __init__(self, row, column):
        super().__init__()
        size = 50
        self.setMinimumSize(QSize(size, size))
        self.setMaximumSize(QSize(size, size))
        self.row = row
        self.column = column
        self.pawn = Pawn.Empty
        self.callback = lambda field: print("not define")
        self.clicked.connect(self.on_click)
        self.set_field_color()
        self.setStyleSheet(self.styleSheet() + ";font-size: 30px")

    def set_field_color(self):
        row_parity = (self.row % 2) == 0
        column_parity = (self.column % 2) == 0
        if \
                column_parity and not row_parity \
                        or \
                        row_parity and not column_parity:

            self.setStyleSheet("background-color: grey")
        else:
            self.setStyleSheet("background-color: cornsilk")

    def activate(self):
        self.setStyleSheet(self.styleSheet() + ";border: 3px dashed blue;")

    def deactivate(self):
        self.setStyleSheet(self.styleSheet() + ";border: none")

    def possible(self):
        self.setStyleSheet(self.styleSheet() + ";border: 3px dashed green;")

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
