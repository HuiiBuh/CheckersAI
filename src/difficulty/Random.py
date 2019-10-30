from random import randrange

from difficulty.Opponent import Opponent


class Random(Opponent):
    """
    A Random game
    """

    def _make_next_move(self) -> None:
        """
        Make a random next moves
        :return: None
        """

        # Check if it is the turn of the computer
        if self.game.whose_turn() is not self.player:
            return

        # Get all possible moves
        possible_moves: list = self.game.get_possible_moves()

        # Count the Moves and randomly select the right move
        move_count: int = len(possible_moves)
        take_move = randrange(move_count)

        # Move a piece
        print(f"Moved: {self._position_to_coordinates(possible_moves[take_move][0])}"
              f"/{self._position_to_coordinates(possible_moves[take_move][1])}")
        self.game.move(possible_moves[take_move])
