class Move:
    def __init__(self, source_field, destination_field, pawn_to_capture=None):
        self.source_field = source_field
        self.destination_field = destination_field
        self.pawn_to_capture = pawn_to_capture

    def __eq__(self, other):
        return self.source_field == other.source_field and \
            self.pawn_to_capture == other.pawn_to_capture and \
            self.destination_field == other.destination_field

    def __hash__(self):
        return hash(hash(self.source_field)+hash(self.destination_field)+hash(self.pawn_to_capture))
