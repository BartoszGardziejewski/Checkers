import random

from game.movement_manager import MovementManager
from widgets.board_field import Pawn


class AbstractStrategy:

    def __init__(self, ai, enemy, board):
        self.ai = ai
        self.enemy = enemy
        self.board = board

    def evaluate_moves_weights(self, possible_moves):
        capturing_moves = MovementManager.extract_capturing_moves(possible_moves)
        if capturing_moves:
            return random.choice(self._get_best_capturing_moves(capturing_moves))
        elif possible_moves:
            return random.choice(self._get_best_no_capturing_moves(possible_moves))
        else:
            print('No possible moves for AI')
            return None

    def _get_best_no_capturing_moves(self, possible_moves):
        moves_with_weights = []

        for possible_move in possible_moves:
            if possible_move.source_field.pawn in {Pawn.Black, Pawn.White}:
                weight = self._get_weights_for_normal_pawn_move(possible_move)
            else:
                weight = self._get_weights_for_queen_move(possible_move)
            moves_with_weights.append(MoveWithWeight(possible_move, weight))

        return self._gen_moves_with_maximum_weight(moves_with_weights)

    def _get_weights_for_normal_pawn_move(self, move):
        pass

    def _get_weights_for_queen_move(self, move):
        pass

    def _get_best_capturing_moves(self, possible_moves):
        moves_with_weights = []

        for possible_move in possible_moves:
            if possible_move.source_field.pawn in {Pawn.Black, Pawn.White}:
                weight = self._get_weights_for_normal_pawn_capturing_move(possible_move)
            else:
                weight = self._get_weights_for_queen_capturing_move(possible_move)
            moves_with_weights.append(MoveWithWeight(possible_move, weight))

        return self._gen_moves_with_maximum_weight(moves_with_weights)

    def _get_weights_for_normal_pawn_capturing_move(self, move):
        pass

    def _get_weights_for_queen_capturing_move(self, move):
        pass

    def _if_pawn_can_be_captured_after_move(self, move):
        move.destination_field.put_pawn(move.source_field.pawn)
        move.source_field.remove_pawn()
        can_be_captured = self._if_pawn_can_be_captured_on_this_field(move.destination_field)
        move.source_field.put_pawn(move.destination_field.pawn)
        move.destination_field.remove_pawn()
        return can_be_captured

    def _if_pawn_can_be_captured_on_this_field(self, field):
        adjacent_fields = self.board.get_adjacent_fields(field)
        for adjacent_field in adjacent_fields:
            if adjacent_field.pawn not in [Pawn.Empty] and adjacent_field.pawn not in self.ai.pawns:
                enemy_possible_moves = MovementManager.eval_moves(self.board, adjacent_field, self.enemy)
                enemy_capturing_moves = MovementManager.extract_capturing_moves(enemy_possible_moves)
                if len(enemy_capturing_moves) > 0:
                    for enemy_capturing_move in enemy_capturing_moves:
                        if enemy_capturing_move.pawn_to_capture == field:
                            return True
        return False

    def _get_capturing_moves_after_move(self, move):
        next_possible_moves = MovementManager\
            .eval_abstract_moves(
                self.board, move.destination_field,
                self.ai, move.source_field.pawn
            )
        return MovementManager.extract_capturing_moves(next_possible_moves)

    def _gen_moves_with_maximum_weight(self, moves_with_weights):
        moves_with_weights.sort(key=lambda move: move.weight, reverse=True)
        selected_moves = list()
        min_val = moves_with_weights[0].weight
        for move_with_weight in moves_with_weights:
            if move_with_weight.weight == min_val:
                selected_moves.append(move_with_weight.move)
            else:
                break

        return selected_moves

    @staticmethod
    def name():
        return "abstract strategy !!! should not be used !!!"


class MoveWithWeight:
    def __init__(self, move, weight):
        self.move = move
        self.weight = weight
