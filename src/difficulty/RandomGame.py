import math

from checkers.game import Game
from random import randrange


class RandomGame:
    """
    A Random game
    """

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
        Move a pice
        :param start_position: The starting coordinates of the pice
        :param end_position: The end coordinates of the pice
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

        possible_moves = self.game.get_possible_moves()

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

        ymod = -1 + (y % 2)
        mod = (position % 4)

        if mod != 0:
            x = 2 * mod + ymod
        else:
            x = 8 + ymod

        return x, y

    def _make_next_move(self) -> None:
        """
        Make a random next move
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

        # Move a pice
        print(f"Moved: {self._position_to_coordinates(possible_moves[take_move][0])}"
              f"/{self._position_to_coordinates(possible_moves[take_move][1])}")
        self.game.move(possible_moves[take_move])
