from PyQt5.QtWidgets import QGridLayout

from widgets.board_field import BoardField


class Board(QGridLayout):

    def __init__(self):
        super().__init__()
        board_fields = []
        for row in range(0, 8):
            for column in range(0, 8):
                board_field = BoardField(row, column)
                board_fields.append(board_field)
                self.addWidget(board_field, row, column)
