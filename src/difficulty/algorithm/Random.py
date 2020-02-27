import random

from difficulty.algorithm.Opponent import Opponent


class Random(Opponent):
    """
    A Random game
    """

    def make_next_move(self) -> None:
        """
        Make a random next moves
        :return: None
        """

        # Check if it is the turn of the computer
        if self.game.whose_turn() is not self.player:
            return

        # Get a random move
        possible_moves = self.game.get_possible_moves()
        move = random.sample(possible_moves, len(possible_moves))[0]

        # Move a piece
        self.game.move(move)
