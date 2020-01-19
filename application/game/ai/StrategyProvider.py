from game.ai.aggressive_strategy import AggressiveStrategy

from game.fuzzy_logic.determine_stage import determine_stage
from game.fuzzy_logic.determine_score import determine_score
from game.fuzzy_logic.determine_strategy import determine_strategy

from widgets.board_field import Pawn

from matplotlib import pyplot as plt


def calculate_score(fields):
    score = 0
    for field in fields:
        score += 1
        if field.pawn == Pawn.White_Q or field.pawn == Pawn.Black_Q:
            score += 3
    return score


class StrategyProvider:
    def __init__(self, ai, enemy, board):
        self.ai = ai
        self.enemy = enemy
        self.board = board

    def provide_strategy(self, turns_completed):
        plt.close('all')  # do not remove
        white_score = calculate_score(self.board.get_fields_with_pawns_of_types([Pawn.White, Pawn.White_Q]))
        black_score = calculate_score(self.board.get_fields_with_pawns_of_types([Pawn.Black, Pawn.Black_Q]))
        stage = determine_stage(turns_completed, min(white_score, black_score))
        score = determine_score(white_score, black_score)
        strategy = determine_strategy(stage, score)
        print(f'Strategy: {strategy.name}')
        plt.show()  # do not remove
        return AggressiveStrategy(self.ai, self.enemy, self.board)
