import math

from checkers.game import Game


class Opponent:
    def __init__(self, player: int):
        """
        Generate a new Random game
        :param player: The player of the RandomGame (1 or 2)
        """
        self.player = player
        self.game = Game()

    def __repr__(self) -> Game:
        """
        Returns the game
        :return: The currently playing game
        """
        return self.game

    def __history__(self) -> list:
        """
        Returns the history of the game
        :return: List of moves that happened in the game
        """
        return self.game.moves

    def start(self):
        """
        Start the game
        :return: None
        """
        if self.game.whose_turn() is self.player:
            self._make_next_move()
        else:
            print("It is your turn")

    def move(self, start_position: tuple, end_position: tuple):
        """
        Move a piece
        :param start_position: The starting coordinates of the piece
        :param end_position: The end coordinates of the piece
        :return: Success
        """

        # Check if it is the turn of the user
        if self.game.whose_turn() is self.player:
            raise PermissionError("It is not your turn")

        # Check if the input is in the right range
        if not (0 < start_position[0] < 9 or 0 < start_position[1] < 9
                or 0 < end_position[0] < 9 or 0 < end_position[1] < 9):
            raise ValueError("The position is only allowed to be between 1 and 8")

        # Create the move tuple
        move: list = [self._coordinates_to_position(start_position), self._coordinates_to_position(end_position)]

        # Check if the move is possible
        if move not in self.game.get_possible_moves():
            raise PermissionError("The move you tried is not possible")

        # Do the move
        self.game.move(move)
        self._make_next_move()
        return True

    @staticmethod
    def _coordinates_to_position(x_y: tuple) -> int:
        """
        Takes the coordinates and transforms them into the checkers position
        :param x_y: X and Y Coordinates
        :return: The checkers position equivalent to the coordinates
        """
        position: int = (x_y[1] - 1) * 4
        position += int(x_y[0] / 2 + 1)
        return position

    @staticmethod
    def _position_to_coordinates(position: int) -> tuple:
        """
        Converts the checkers position into coordinates
        :param position: The position in checkers notation
        :return: The X and Y coordinates
        """

        y = math.ceil((position / 4))

        y_mod = -1 + (y % 2)
        mod = (position % 4)

        if mod != 0:
            x = 2 * mod + y_mod
        else:
            x = 8 + y_mod

        return x, y

    def _make_next_move(self):
        pass
