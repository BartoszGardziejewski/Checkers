from widgets.board_field import Pawn
from game.move import Move


class MovementManager:

    @staticmethod
    def eval_abstract_moves(board, source_field, player, pawn):
        possible_moves = list()
        possible_row_shifts = MovementManager.get_possible_row_shifts(pawn)
        possible_col_shifts = [-1, 1]

        for row_shift in possible_row_shifts:
            for col_shift in possible_col_shifts:
                MovementManager._check_possible_moves_for_shift(
                    board, possible_moves, player,
                    source_field, col_shift, row_shift
                )

        return possible_moves

    @staticmethod
    def eval_moves(board, source_field, player):
        possible_moves = list()
        possible_row_shifts = MovementManager.get_possible_row_shifts(source_field.pawn)
        possible_col_shifts = [-1, 1]

        for row_shift in possible_row_shifts:
            for col_shift in possible_col_shifts:
                MovementManager._check_possible_moves_for_shift(
                    board, possible_moves, player,
                    source_field, col_shift, row_shift
                )

        return possible_moves

    @staticmethod
    def _check_possible_moves_for_shift(board, possible_moves, player, source_field, col_shift, row_shift):
        row = source_field.row
        column = source_field.column
        new_col = column + col_shift
        new_row = row + row_shift
        shifted_field = MovementManager._get_field_to_shift_to(board, new_col, new_row)
        if shifted_field:
            if shifted_field.pawn == Pawn.Empty:
                possible_moves.append(Move(source_field, shifted_field))
            elif shifted_field.pawn not in player.pawns:
                new_doubly_col = column + 2 * col_shift
                new_doubly_row = row + 2 * row_shift
                doubly_shifted_field = MovementManager._get_field_to_shift_to(board, new_doubly_col, new_doubly_row)
                if doubly_shifted_field:
                    if doubly_shifted_field.pawn == Pawn.Empty:
                        possible_moves.append(
                            Move(source_field, doubly_shifted_field, pawn_to_capture=shifted_field))

    @staticmethod
    def _get_field_to_shift_to(board, new_col, new_row):
        if (0 <= new_col < board.size) and (0 <= new_row < board.size):
            return board.board_fields[new_row][new_col]
        else:
            return None

    @staticmethod
    def get_possible_row_shifts(pawn):
        if pawn == Pawn.White_Q or pawn == Pawn.Black_Q:
            return [-1, 1]
        elif pawn == Pawn.White:
            return [-1]
        elif pawn == Pawn.Black:
            return [1]

    @staticmethod
    def get_possible_moves_for_player(board, player):
        possible_source_fields = board.get_fields_with_pawns_of_types(player.pawns)
        possible_moves = list()
        for possible_source_field in possible_source_fields:
            moves_per_field = MovementManager.eval_moves(board, possible_source_field, player)
            if moves_per_field:
                possible_moves.extend(moves_per_field)

        return possible_moves

    @staticmethod
    def extract_capturing_moves(possible_moves):
        return [move for move in possible_moves if move.pawn_to_capture]