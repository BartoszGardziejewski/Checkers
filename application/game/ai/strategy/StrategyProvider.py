import random

from matplotlib import pyplot as plt

from game.ai.strategy.aggressive_strategy import AggressiveStrategy
from game.ai.strategy.defensive_strategy import DefensiveStrategy
from game.ai.strategy.slightly_defensive_strategy import SlightlyDefensiveStrategy
from game.ai.strategy.slightly_aggressive_strategy import SlightlyAggressiveStrategy

from game.fuzzy_logic.determine_score import determine_score
from game.fuzzy_logic.determine_stage import determine_stage
from game.fuzzy_logic.determine_strategy import determine_strategy
from game.fuzzy_logic.determine_strategy import Strategy


class StrategyProvider:

    def __init__(self, ai, enemy, board):
        self.ai = ai
        self.enemy = enemy
        self.board = board
        self.map_of_possible_strategies = {
            Strategy.aggressive: AggressiveStrategy,
            Strategy.defensive: DefensiveStrategy,
            Strategy.slightly_defensive: SlightlyDefensiveStrategy,
            Strategy.slightly_aggressive: SlightlyAggressiveStrategy
        }

    def provide_strategy(self, turns_completed, white_pawns, black_pawns):
        plt.close('all')  # do not remove! for graph purposes
        losing_player_pieces = white_pawns if white_pawns < black_pawns else black_pawns
        fuzzy_strategy = determine_strategy(
            determine_stage(turns_completed, losing_player_pieces),
            determine_score(white_pawns, black_pawns)
        )
        print(f'Strategy: {fuzzy_strategy.name}')
        strategy = self.map_of_possible_strategies[fuzzy_strategy]
        plt.show()  # do not remove! for graph purposes
        return strategy(self.ai, self.enemy, self.board)
