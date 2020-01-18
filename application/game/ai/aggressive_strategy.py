import random
from copy import deepcopy

from game.movement_manager import MovementManager
from game.ai.strategy import AbstractStrategy
from game.ai.strategy import MoveWithWeight
from widgets.board_field import Pawn


class AggressiveStrategy(AbstractStrategy):

    def __init__(self, ai, enemy, board):
        super().__init__(ai, enemy, board)

    def evaluate_moves_weights(self, possible_moves):
        moves_with_weights = []
        capturing_moves = MovementManager.extract_capturing_moves(possible_moves)
        if capturing_moves:

            for capturing_move in capturing_moves:
                weight = 10
                next_capturing_moves = self._get_capturing_moves_after_move(capturing_move)
                if next_capturing_moves:
                    weight = weight + 5
                moves_with_weights.append(MoveWithWeight(capturing_move, weight))

            return random.choice(self._gen_moves_with_maximum_weight(moves_with_weights))

        elif possible_moves:

            for possible_move in possible_moves:
                if possible_move.source_field.pawn in {Pawn.Black, Pawn.White}:
                    weight = 5 + possible_move.destination_field.row
                    if self._if_pawn_can_be_captured_after_move(possible_move):
                        weight = 1
                    else:
                        next_capturing_moves = self._get_capturing_moves_after_move(possible_move)
                        if next_capturing_moves:
                            weight = weight + 5
                else:
                    weight = 5
                    if self._if_pawn_can_be_captured_after_move(possible_move):
                        weight = 0
                    else:
                        next_capturing_moves = self._get_capturing_moves_after_move(possible_move)
                        if next_capturing_moves:
                            weight = weight + 5
                moves_with_weights.append(MoveWithWeight(possible_move, weight))

            return random.choice(self._gen_moves_with_maximum_weight(moves_with_weights))

        else:
            print('No possible moves for AI')
            return None

    def _get_capturing_moves_after_move(self, move):
        next_possible_moves = MovementManager\
            .eval_abstract_moves(
                self.board, move.destination_field,
                self.ai, move.source_field.pawn
            )
        return MovementManager.extract_capturing_moves(next_possible_moves)

    def _if_pawn_can_be_captured_after_move(self, move):
        move.destination_field.put_pawn(move.source_field.pawn)
        move.source_field.remove_pawn()
        adjacent_fields = self.board.get_adjacent_fields(move.destination_field)
        for field in adjacent_fields:
            if field.pawn not in [Pawn.Empty] and field.pawn not in self.ai.pawns:
                enemy_possible_moves = MovementManager.eval_moves(self.board, field, self.enemy)
                enemy_capturing_moves = MovementManager.extract_capturing_moves(enemy_possible_moves)
                if len(enemy_capturing_moves) > 0:
                    move.source_field.put_pawn(move.destination_field.pawn)
                    move.destination_field.remove_pawn()
                    return True

        move.source_field.put_pawn(move.destination_field.pawn)
        move.destination_field.remove_pawn()
        return False

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
