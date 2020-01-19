from game.ai.aggressive_strategy import AggressiveStrategy

from game.fuzzy_logic.determine_stage import determine_stage
from game.fuzzy_logic.determine_score import determine_score
from game.fuzzy_logic.determine_strategy import determine_strategy

from widgets.board_field import Pawn


class StrategyProvider:

    def __init__(self, ai, enemy, board):
        self.ai = ai
        self.enemy = enemy
        self.board = board

    def provide_strategy(self, turns_completed):
        white_score = len(self.board.get_fields_with_pawns_of_type(Pawn.White))
        black_score = len(self.board.get_fields_with_pawns_of_type(Pawn.Black))
        stage = determine_stage(turns_completed, white_score + black_score)
        score = determine_score(white_score, black_score)
        strategy = determine_strategy(stage, score)
        print(strategy.name)
        return AggressiveStrategy(self.ai, self.enemy, self.board)
