from PyQt5.QtWidgets import QWidget

from widgets.board import Board


class Application(QWidget):

    def __init__(self):
        super().__init__()
        board = Board()
        self.setLayout(board)
