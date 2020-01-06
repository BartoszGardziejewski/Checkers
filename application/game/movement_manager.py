from widgets.board_field import Pawn
from game.move import Move


class MovementManager:
    black_row_shifts = [1]
    white_row_shifts = [-1]
    col_shifts = [-1, 1]

    @staticmethod
    def eval_moves(board, from_field, player):
        possible_moves = []
        row = from_field.row
        column = from_field.column

        possible_row_shifts = list()
        if player.pawn == Pawn.White:
            possible_row_shifts = MovementManager.white_row_shifts
        elif player.pawn == Pawn.Black:
            possible_row_shifts = MovementManager.black_row_shifts

        for row_shift in possible_row_shifts:
            for col_shift in MovementManager.col_shifts:
                try:
                    if board.board_fields[row + row_shift][column + col_shift].pawn == Pawn.Empty:
                        possible_moves.append(Move(from_field, board.board_fields[row + row_shift][column + col_shift]))
                    elif board.board_fields[row + row_shift][column + col_shift].pawn != player.pawn:
                        if board.board_fields[row + row_shift * 2][column + col_shift * 2].pawn == Pawn.Empty:
                            possible_moves.append(
                                Move(from_field, board.board_fields[row + row_shift * 2][column + col_shift * 2],
                                     board.board_fields[row + row_shift][column + col_shift]))
                except IndexError:
                    print("")

        return possible_moves
