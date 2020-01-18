from application.fuzzy_logic.determine_stage import *
from application.fuzzy_logic.determine_score import *
from application.fuzzy_logic.determine_strategy import *


def prioritize_moves(board, possible_moves, completed_turns_number):
    white_score = len(self.board.get_fields_with_pawns_of_type(Pawn.White))
    black_score = len(self.board.get_fields_with_pawns_of_type(Pawn.Black))
    stage = determine_stage(completed_turns_number, white_score + black_score)
    score = determine_score(white_score, black_score)
    strategy = determine_strategy(stage, score)
    print(strategy)
    pass
