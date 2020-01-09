from itertools import cycle

from widgets.board_field import Pawn
from game.player import Player
from game.ai import AiPlayer
from game.movement_manager import MovementManager


class Game():
    def __init__(self, board, white_player=Player(Pawn.White), black_player=AiPlayer(Pawn.Black)):
        self.board = board
        self.board.set_all_callbacks(self.activate_source_field)
        self.players = cycle([white_player, black_player])
        self.current_player = next(self.players)
        self.active_field = None
        self.possible_moves = list()
        self.white_score, self.black_score = self.update_scores()

    def activate_source_field(self, field):
        if not self.board.get_possible_source_fields(self.current_player.pawn):
            print(f'{self.current_player.pawn} has no more pawns to use')
        elif field.pawn == self.current_player.pawn:
            field.activate()
            self.active_field = field
            self.possible_moves = MovementManager.eval_moves(self.board, self.active_field, self.current_player)
            for possible_move in self.possible_moves:
                possible_move.destination_field.mark_as_possible()
            self.board.set_all_callbacks(self.activate_destination_field)
        else:
            print("wrong field")

    def activate_destination_field(self, field):
        if field == self.active_field:
            self.deactivate_field()
        elif field.pawn == self.current_player.pawn:
            self.deactivate_field()
            self.activate_source_field(field)
        else:
            possible_move = next((move for move in self.possible_moves if move.destination_field == field), None)
            if possible_move is None:
                print("move not possible")
            else:
                self.active_field.remove_pawn()
                field.put_pawn(self.current_player.pawn)
                if possible_move.pawn_to_capture:
                    possible_move.pawn_to_capture.remove_pawn()
                self.deactivate_field()
                self.move_ai()
        self.update_scores()

    def deactivate_field(self):
        self.active_field.deactivate()
        for possible_moves in self.possible_moves:
            possible_moves.destination_field.deactivate()
        self.possible_moves = list()
        self.board.set_all_callbacks(self.activate_source_field)

    def move_ai(self):
        self.current_player = next(self.players)
        self.current_player.make_move(self.board)
        self.current_player = next(self.players)

    def update_scores(self):
        white_score = self.board.get_possible_source_fields(Pawn.White)
        black_score = self.board.get_possible_source_fields(Pawn.Black)
        print(f'white_pieces: {len(white_score)}; black_pieces: {len(black_score)}')
        return white_score, black_score
