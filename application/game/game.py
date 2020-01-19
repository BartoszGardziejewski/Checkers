from itertools import cycle

from widgets.board_field import BoardField
from widgets.board_field import Pawn
from game.player import Player
from game.ai.ai import AiPlayer
from game.ai.strategy.StrategyProvider import StrategyProvider
from game.movement_manager import MovementManager


class Game:
    def __init__(self, board,
                 white_player=Player([Pawn.White, Pawn.White_Q]),
                 black_player=AiPlayer([Pawn.Black, Pawn.Black_Q])):
        self.board = board
        self.board.set_all_callbacks(self.activate_source_field)
        self.players = cycle([white_player, black_player])
        self.current_player = next(self.players)
        self.strategy_provider = StrategyProvider(black_player, white_player, board)
        self.active_field = None
        self.mandatory_moves = list()
        self.possible_moves = list()
        self.turns_completed = 0
        self.white_score, self.black_score = self.update_scores()

    def _start_new_turn(self):
        self._check_mandatory_capture()
        self._mark_mandatory_moves()

    def _mark_mandatory_moves(self):
        if len(self.mandatory_moves) > 0:
            for mandatory_move in self.mandatory_moves:
                mandatory_move.source_field.mark_as_mandatory()

    def activate_source_field(self, field):
        if not self.board.get_fields_with_pawns_of_types(self.current_player.pawns):
            print(f'{self.current_player.pawn} has no more pawns to use')
        elif field.pawn in self.current_player.pawns:
            field.activate()
            self.active_field = field
            self.possible_moves = MovementManager.eval_moves(self.board, self.active_field, self.current_player)
            if len(self.mandatory_moves) > 0:
                print("there are mandatory moves")
                self.possible_moves = set(self.mandatory_moves).intersection(set(self.possible_moves))
            for possible_move in self.possible_moves:
                possible_move.destination_field.mark_as_possible()
            self.board.set_all_callbacks(self.activate_destination_field)
        else:
            print("wrong field")

    def activate_destination_field(self, field):
        if field == self.active_field:
            self.deactivate_field()
        elif field.pawn in self.current_player.pawns:
            self.deactivate_field()
            self.activate_source_field(field)
        else:
            possible_move = next((move for move in self.possible_moves if move.destination_field == field), None)
            if possible_move is None:
                print("move not possible")
            else:
                self._make_a_move(field, possible_move)
                if len(self.mandatory_moves) == 0:
                    self._end_turn()

    def _end_turn(self):
        self.current_player = next(self.players)
        self.turns_completed += 1
        self.move_ai()
        self.white_score, self.black_score = self.update_scores()
        self._start_new_turn()

    def _make_a_move(self, field, possible_move):
        field.put_pawn(possible_move.source_field.pawn)
        self.active_field.remove_pawn()
        self.deactivate_field()
        self.mandatory_moves.clear()
        if possible_move.pawn_to_capture:
            possible_move.pawn_to_capture.remove_pawn()
            possible_next_move = MovementManager.eval_moves(self.board, field, self.current_player)
            self.mandatory_moves = MovementManager.extract_capturing_moves(possible_next_move)
            if len(self.mandatory_moves) > 0:
                field.mark_as_mandatory()
        if BoardField.should_the_pawn_be_crowned(field):
            BoardField.crowning_the_pawn(field)

    def _check_mandatory_capture(self):
        possible_moves = MovementManager.get_possible_moves_for_player(self.board, self.current_player)
        self.mandatory_moves = MovementManager.extract_capturing_moves(possible_moves)

    def deactivate_field(self):
        self.active_field.deactivate()
        for possible_moves in self.possible_moves:
            possible_moves.destination_field.deactivate()
        self.possible_moves = list()
        self.board.set_all_callbacks(self.activate_source_field)

    def move_ai(self):
        strategy = self.strategy_provider.provide_strategy(
            self.turns_completed, len(self.white_score), len(self.black_score)
        )
        was_pawn_captured = self.current_player.make_move(self.board, strategy)
        while was_pawn_captured:
            was_pawn_captured = self.current_player.make_next_move(self.board, strategy)
        self.current_player = next(self.players)
        self.turns_completed += 1

    def update_scores(self):
        white_score = self.board.get_fields_with_pawns_of_types([Pawn.White, Pawn.White_Q])
        black_score = self.board.get_fields_with_pawns_of_types([Pawn.Black, Pawn.Black_Q])
        print()
        print(
            f'turns_completed: {self.turns_completed}; white_pieces: {len(white_score)}; black_pieces: {len(black_score)}')
        return white_score, black_score
