import random

from game.player import Player
from game.movement_manager import MovementManager


def get_moves_that_capture(possible_moves):
    return [move for move in possible_moves if move.pawn_to_capture]


class AiPlayer(Player):
    def __init__(self, pawn):
        super().__init__(pawn)

    def make_move(self, board):
        chosen_move = self.choose_move(board)
        chosen_move.source_field.remove_pawn()
        chosen_move.destination_field.put_pawn(self.pawn)
        if chosen_move.pawn_to_capture:
            chosen_move.pawn_to_capture.remove_pawn()

    def choose_move(self, board):
        possible_source_fields = board.get_possible_source_fields(self.pawn)
        possible_moves = list()
        for possible_source_field in possible_source_fields:
            moves_per_field = MovementManager.eval_moves(board, possible_source_field, self)
            if moves_per_field:
                possible_moves.extend(moves_per_field)

        capturing_moves = get_moves_that_capture(possible_moves)
        if capturing_moves:
            return random.choice(capturing_moves)
        if possible_moves:
            return random.choice(possible_moves)
        else:
            print('ERROR: No possible moves for AI')
