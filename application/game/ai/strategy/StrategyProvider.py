import random

from game.ai.strategy.aggressive_strategy import AggressiveStrategy
from game.ai.strategy.defensive_strategy import DefenciveStrategy


class StrategyProvider:

    def __init__(self, ai, enemy, board):
        self.ai = ai
        self.enemy = enemy
        self.board = board

    def provide_strategy(self):
        possible_strategies = [
            AggressiveStrategy,
            DefenciveStrategy
        ]
        strategy = random.choice(possible_strategies)
        print(strategy.name())
        return strategy(self.ai, self.enemy, self.board)
