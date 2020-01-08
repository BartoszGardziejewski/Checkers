from widgets.board_field import Pawn
from game.move import Move


class MovementManager:
    @staticmethod
    def eval_moves(board, source_field, player):
        possible_moves = list()
        row = source_field.row
        column = source_field.column

        possible_row_shifts = MovementManager.get_possible_row_shifts(player)
        possible_col_shifts = [-1, 1]

        for row_shift in possible_row_shifts:
            for col_shift in possible_col_shifts:
                try:
                    shifted_field = board.board_fields[row + row_shift][column + col_shift]
                    if shifted_field.pawn == Pawn.Empty:
                        possible_moves.append(Move(source_field, shifted_field))
                    elif shifted_field.pawn != player.pawn:
                        doubly_shifted_field = board.board_fields[row + 2 * row_shift][column + 2 * col_shift]
                        if doubly_shifted_field.pawn == Pawn.Empty:
                            possible_moves.append(
                                Move(source_field, doubly_shifted_field, pawn_to_capture=shifted_field))
                except IndexError as e:
                    print(f"MovementManager raised an exception: {e}")

        return possible_moves

    @staticmethod
    def get_possible_row_shifts(player):
        white_row_shifts = [-1]
        black_row_shifts = [1]

        if player.pawn == Pawn.White:
            return white_row_shifts
        elif player.pawn == Pawn.Black:
            return black_row_shifts
