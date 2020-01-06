from PyQt5.QtWidgets import QGridLayout

from widgets.board_field import BoardField


class Board(QGridLayout):
    def __init__(self):
        super().__init__()
        self.board_fields = [[]]
        for row in range(0, 8):
            self.board_fields.append([])
            for column in range(0, 8):
                board_field = BoardField(row, column)
                self.board_fields[row].append(board_field)
                self.addWidget(board_field, row, column)

    def add_pawn(self, row, column, pawn):
        self.board_fields[row][column].put_pawn(pawn)

    def set_all_callbacks(self, callback):
        for board_fields in self.board_fields:
            for board_field in board_fields:
                board_field.set_clicked_callback(callback)
