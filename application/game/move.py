class Move:
    def __init__(self, source_field, destination_field, pawn_to_capture=None):
        self.source_field = source_field
        self.destination_field = destination_field
        self.pawn_to_capture = pawn_to_capture
