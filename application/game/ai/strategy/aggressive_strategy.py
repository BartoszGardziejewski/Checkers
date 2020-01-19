from game.ai.strategy.strategy import AbstractStrategy
from widgets.board_field import Pawn


class AggressiveStrategy(AbstractStrategy):

    def __init__(self, ai, enemy, board):
        super().__init__(ai, enemy, board)

    def _get_weights_for_normal_pawn_move(self, possible_move):
        weight = 3 + possible_move.destination_field.row
        if self._if_pawn_can_be_captured_after_move(possible_move):
            weight = 1
        else:
            if self._if_pawn_can_be_captured_on_this_field(possible_move.source_field):
                weight = weight + 3
            weight = weight + self._get_weights_of_possible_capture(possible_move)
        return weight

    def _get_weights_for_queen_move(self, possible_move):
        if possible_move.destination_field.row < 4:
            weight = 4 + \
                     (possible_move.destination_field.row - possible_move.source_field.row) *\
                     4-possible_move.source_field.row
        else:
            weight = 4 + \
                     (possible_move.source_field.row - possible_move.destination_field.row) * \
                     possible_move.source_field.row - 4
        if self._if_pawn_can_be_captured_after_move(possible_move):
            weight = 0
        else:
            if self._if_pawn_can_be_captured_on_this_field(possible_move.source_field):
                weight = weight + 5
            weight = weight + self._get_weights_of_possible_capture(possible_move)
        return weight

    def _get_weights_for_normal_pawn_capturing_move(self, capturing_move):
        weight = 10
        if capturing_move.pawn_to_capture in {Pawn.White_Q, Pawn.Black_Q}:
            weight = weight + 8
        weight = weight + self._get_weights_of_possible_capture(capturing_move)
        if self._if_pawn_can_be_captured_on_this_field(capturing_move.source_field):
            weight = weight + 3
        return weight

    def _get_weights_for_queen_capturing_move(self, capturing_move):
        weight = 10
        if capturing_move.pawn_to_capture in {Pawn.White_Q, Pawn.Black_Q}:
            weight = weight + 6
        weight = weight + self._get_weights_of_possible_capture(capturing_move)
        if self._if_pawn_can_be_captured_on_this_field(capturing_move.source_field):
            weight = weight + 5
        return weight

    def _get_weights_of_possible_capture(self, move):
        weight = 0
        next_capturing_moves = self._get_capturing_moves_after_move(move)
        if next_capturing_moves:
            weight = weight + 5
            for next_capturing_move in next_capturing_moves:
                if next_capturing_move.pawn_to_capture in {Pawn.White_Q, Pawn.Black_Q}:
                    weight = weight + 4
        return weight

    @staticmethod
    def name():
        return "AggressiveStrategy"
