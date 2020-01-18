from PyQt5.QtWidgets import QGridLayout

from widgets.board_field import BoardField, Pawn


class Board(QGridLayout):
    def __init__(self):
        super().__init__()
        self.board_fields = list(list())
        self.size = 8
        for row in range(0, self.size):
            self.board_fields.append(list())
            for column in range(0, 8):
                board_field = BoardField(row, column)
                self.board_fields[row].append(board_field)
                self.addWidget(board_field, row, column)

        for row in range(0, 3):
            for column in range(1, 9, 2):
                self.add_pawn(row, column - (row % 2), Pawn.Black)

        for row in range(5, 8):
            for column in range(1, 9, 2):
                self.add_pawn(row, column - (row % 2), Pawn.White)

    def add_pawn(self, row, column, pawn):
        self.board_fields[row][column].put_pawn(pawn)

    def get_fields_with_pawns_of_types(self, pawns):
        fields = []
        for pawn in pawns:
            fields = fields + self.get_fields_with_pawns_of_type(pawn)

        return fields

    def get_fields_with_pawns_of_type(self, pawn):
        possible_source_fields = list()
        for fields in self.board_fields:
            for field in fields:
                if field.pawn == pawn:
                    possible_source_fields.append(field)
        return possible_source_fields

    def set_all_callbacks(self, callback):
        for board_fields in self.board_fields:
            for board_field in board_fields:
                board_field.set_clicked_callback(callback)
