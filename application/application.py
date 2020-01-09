from PyQt5.QtWidgets import QWidget

from widgets.board import Board

from game.game import Game


class Application(QWidget):

    def __init__(self):
        super().__init__()
        self.board = Board()
        self.setLayout(self.board)
        self.game = Game(self.board)
