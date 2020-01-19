
from game.ai.aggressive_strategy import AggressiveStrategy


class StrategyProvider:

    def __init__(self, ai, enemy, board):
        self.ai = ai
        self.enemy = enemy
        self.board = board

    def provide_strategy(self, turns_completed):
        # Do fuzzy logic stuff here :)
        return AggressiveStrategy(self.ai, self.enemy, self.board)