import random

from game.movement_manager import MovementManager
from game.ai.strategy import AbstractStrategy


class RandomStrategy(AbstractStrategy):

    @staticmethod
    def evaluate_moves_weights(possible_moves, board):
        capturing_moves = MovementManager.extract_capturing_moves(possible_moves)
        if capturing_moves:
            return random.choice(capturing_moves)
        if possible_moves:
            return random.choice(possible_moves)
        else:
            print('No possible moves for AI')
            return None

