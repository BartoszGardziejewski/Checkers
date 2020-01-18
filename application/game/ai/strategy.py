class AbstractStrategy:

    def __init__(self, ai, enemy, board):
        self.ai = ai
        self.enemy = enemy
        self.board = board

    def evaluate_moves_weights(self, possible_moves, board, player):
        pass


class MoveWithWeight:
    def __init__(self, move, weight):
        self.move = move
        self.weight = weight
