import random

from game.player import Player
from game.movement_manager import MovementManager
from widgets.board_field import Pawn


class AiPlayer(Player):
    def __init__(self, pawn):
        self.last_field = None
        super().__init__(pawn)

    def make_move(self, board):
        chosen_move = self.choose_move(board)
        return self._make_move(chosen_move)

    def _make_move(self, chosen_move):
        was_pawn_capture = False
        chosen_move.source_field.remove_pawn()
        chosen_move.destination_field.put_pawn(self.pawn)
        if chosen_move.pawn_to_capture:
            chosen_move.pawn_to_capture.remove_pawn()
            was_pawn_capture = True
        self.last_field = chosen_move.destination_field
        return was_pawn_capture

    def make_next_move(self, board):
        possible_next_moves = MovementManager.eval_moves(board, self.last_field, self)
        possible_next_moves = MovementManager.extract_capturing_moves(possible_next_moves)
        if len(possible_next_moves) == 0:
            return False
        next_move = random.choice(possible_next_moves)
        return self._make_move(next_move)

    def choose_move(self, board):
        possible_moves = MovementManager.get_possible_moves_for_player(board, self)
        capturing_moves = MovementManager.extract_capturing_moves(possible_moves)
        if capturing_moves:
            return random.choice(capturing_moves)
        if possible_moves:
            return random.choice(possible_moves)
        else:
            print('ERROR: No possible moves for AI')

    def get_opponents_pawn_type(self):
        return Pawn.White if self.pawn is Pawn.Black else Pawn.Black
