from widgets.board_field import Pawn

from game.move import Move


class MovementManager:

    @staticmethod
    def eval_moves(board, from_field, player):
        possible_moves = []
        row = from_field.row
        column = from_field.column

        for row_shift in range(-1, 2, 2):
            for col_shift in range(-1, 2, 2):
                try:
                    if board.board_fields[row + row_shift][column + col_shift].pawn == Pawn.Empty:
                        possible_moves.append(Move(from_field, board.board_fields[row+row_shift][column+col_shift]))
                    elif board.board_fields[row + row_shift][column + col_shift].pawn != player.pawn:
                        if board.board_fields[row + row_shift*2][column + col_shift*2].pawn == Pawn.Empty:
                            possible_moves.append(Move(from_field, board.board_fields[row+row_shift*2][column+col_shift*2], board.board_fields[row + row_shift][column + col_shift]))
                except IndexError:
                    print("")

        return possible_moves
