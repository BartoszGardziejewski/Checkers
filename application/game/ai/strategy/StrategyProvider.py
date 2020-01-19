
from game.ai.strategy.aggressive_strategy import AggressiveStrategy


class StrategyProvider:

    def __init__(self, ai, enemy, board):
        self.ai = ai
        self.enemy = enemy
        self.board = board

    def provide_strategy(self):
        return AggressiveStrategy(self.ai, self.enemy, self.board)