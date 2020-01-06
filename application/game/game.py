from widgets.board_field import Pawn

from game.player import Player

from game.movement_manager import MovementManager


class Game:

    def __init__(self, board, black_player=Player(Pawn.Black), white_player=Player(Pawn.White)):
        self.board = board
        self.board.set_all_callbacks(self.activate_field)
        self.white_player = white_player
        self.black_player = black_player
        self.init_board()
        self.turns = []
        self.turns.append(white_player)
        self.turns.append(black_player)
        self.active_field = None
        self.current_player = None
        self.possible_moves = []

    def init_board(self):
        for row in range(0, 3):
            for column in range(1, 9, 2):
                self.board.add_pawn(row, column-(row % 2), Pawn.Black)

        for row in range(5, 8):
            for column in range(1, 9, 2):
                self.board.add_pawn(row, column-(row % 2), Pawn.White)

    def activate_field(self, field):
        self.current_player = self.turns[0]
        if field.pawn == self.current_player.pawn:
            self.active_field = field
            field.activate()
            self.board.set_all_callbacks(self.move_pawn)
            self.possible_moves = MovementManager.eval_moves(self.board, self.active_field, self.current_player)
            for possible_move in self.possible_moves:
                possible_move.to_field.possible()
        else:
            self.turns[0] = self.current_player
            print("wrong filed")

    def move_pawn(self, field):
        if field == self.active_field:
            self.deactivate_pawn()
        elif field.pawn == self.current_player.pawn:
            self.deactivate_pawn()
            self.activate_field(field)
        else:
            for move in self.possible_moves:
                if field == move.to_field:
                    self.active_field.remove_pawn()
                    field.put_pawn(self.current_player.pawn)
                    self.turns.reverse()
                    if move.paw_to_capture:
                        move.paw_to_capture.remove_pawn()
                    self.deactivate_pawn()
            else:
                print("move not possible")

    def deactivate_pawn(self):
        self.active_field.deactivate()
        for possible_moves in self.possible_moves:
            possible_moves.to_field.deactivate()
        self.possible_moves = []
        self.board.set_all_callbacks(self.activate_field)
