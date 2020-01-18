from enum import Enum

from PyQt5.QtCore import QSize, pyqtSlot
from PyQt5.QtWidgets import QPushButton


class Pawn(Enum):
    Empty = 0,
    White = 1,
    White_Q = 2,
    Black = 3,
    Black_Q = 4,


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
        if pawn == Pawn.Black:
            self.setText('O')
            self.setStyleSheet(self.styleSheet() + ";color: black")
        elif pawn == Pawn.White:
            self.setText('O')
            self.setStyleSheet(self.styleSheet() + ";color: white")
        elif pawn == Pawn.Black_Q:
            self.setText('Q')
            self.setStyleSheet(self.styleSheet() + ";color: black")
        elif pawn == Pawn.White_Q:
            self.setText('Q')
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

    @staticmethod
    def should_the_pawn_be_crowned(field):
        if field.pawn == Pawn.Black_Q or field.pawn == Pawn.White_Q:
            return False
        elif field.pawn == Pawn.White and field.row == 0:
            return True
        elif field.pawn == Pawn.Black and field.row == 7:
            return True
        else:
            return False

    @staticmethod
    def crowning_the_pawn(field):
        if field.pawn == Pawn.Black:
            field.put_pawn(Pawn.Black_Q)
        elif field.pawn == Pawn.White:
            field.put_pawn(Pawn.White_Q)
