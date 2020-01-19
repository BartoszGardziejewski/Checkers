from game.ai.strategy.strategy import AbstractStrategy
from widgets.board_field import Pawn


class SlightlyAggressiveStrategy(AbstractStrategy):

    def __init__(self, ai, enemy, board):
        super().__init__(ai, enemy, board)

    def _get_weights_for_normal_pawn_move(self, possible_move):
        weight = 5
        if self._if_pawn_can_be_captured_after_move(possible_move):
            weight = 1
        else:
            if self._if_pawn_can_be_captured_on_this_field(possible_move.source_field):
                weight = weight + 10
            weight = weight + self._get_weights_of_possible_capture(possible_move, False)
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
                weight = weight + 15
            weight = weight + self._get_weights_of_possible_capture(possible_move, True)
        return weight

    def _get_weights_for_normal_pawn_capturing_move(self, capturing_move):
        weight = 10
        if capturing_move.pawn_to_capture in {Pawn.White_Q, Pawn.Black_Q}:
            weight = weight + 6
        if self._if_pawn_can_be_captured_after_move(capturing_move):
            weight = weight - 2
        if self._if_pawn_can_be_captured_on_this_field(capturing_move.source_field):
            weight = weight + 4
        weight = weight + self._get_weights_of_possible_capture(capturing_move, False)
        return weight

    def _get_weights_for_queen_capturing_move(self, capturing_move):
        weight = 10
        if capturing_move.pawn_to_capture in {Pawn.White_Q, Pawn.Black_Q}:
            weight = weight + 8
        if self._if_pawn_can_be_captured_after_move(capturing_move):
            weight = weight - 4
        if self._if_pawn_can_be_captured_on_this_field(capturing_move.source_field):
            weight = weight + 7
        weight = weight + self._get_weights_of_possible_capture(capturing_move, True)
        return weight

    def _get_weights_of_possible_capture(self, move, is_queen):
        weight = 0
        next_capturing_moves = self._get_capturing_moves_after_move(move)
        if next_capturing_moves:
            weight = weight + 8
            for next_capturing_move in next_capturing_moves:
                if next_capturing_move.pawn_to_capture in {Pawn.White_Q, Pawn.Black_Q}:
                    weight = weight + 6
                if self._if_pawn_can_be_captured_after_move(next_capturing_move):
                    if is_queen:
                        weight = weight - 6
                    else:
                        weight = weight - 2
        return weight

    @staticmethod
    def name():
        return "SlightlyAggressiveStrategy"
