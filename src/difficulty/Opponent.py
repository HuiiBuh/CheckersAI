import math
from abc import ABC, abstractmethod
from time import sleep

from checkers.game import Game

from Colors import COLOUR


class Opponent(ABC):
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

    def play_game(self) -> None:
        """
        Play the game
        :param game: The game object
        :param player: If the user is player one or two
        :return: None
        """

        while not self.game.is_over():
            sleep(0.1)
            if self.game.whose_turn() != self.player:

                start_position: str = input("Start: ")
                end_position: str = input("End: ")

                if not (start_position.isdigit() and end_position.isdigit()):
                    print(COLOUR.RED + "You can only input numbers" + COLOUR.END)
                else:
                    start_position: int = int(start_position)
                    end_position: int = int(end_position)

                    try:
                        self.move(start_position, end_position)
                    except Exception as e:
                        print(COLOUR.RED + str(e) + COLOUR.END + "\n\n")
            else:
                self.make_next_move()

        winner = self.game.get_winner()
        print(COLOUR.GREEN + f"The winner is player {winner}." + COLOUR.END)

    def move(self, start_position: int, end_position: int):
        """
        Move a piece
        :param start_position: The starting coordinates of the piece
        :param end_position: The end coordinates of the piece
        :return: Success
        """

        # Check if it is the turn of the user
        if self.game.whose_turn() is self.player:
            raise PermissionError("It is not your turn")

        # Create the move tuple
        move = [start_position, end_position]

        # Check if the move is possible
        if move not in self.game.get_possible_moves():
            raise PermissionError(f"The move you tried is not possible. {move}")

        # Do the move
        self.game.move(move)
        return True

    @abstractmethod
    def make_next_move(self):
        """
        Has to be overwritten
        :return: None
        """
        raise NotImplementedError("This method has to be overwritten")

    @staticmethod
    def _coordinates_to_position(x_y: list) -> int:
        """
        Takes the coordinates and transforms them into the checkers position
        :param x_y: X and Y Coordinates
        :return: The checkers position equivalent to the coordinates
        """

        # Convert the start char to coordinates
        if ord(x_y[0]) >= 97:
            x_y[0] = ord(x_y[0]) - 96
        else:
            x_y[0] = ord(x_y[0]) - 64

        position: int = (9 - x_y[1] - 1) * 4
        position += math.ceil(x_y[0] / 2)
        return position

    @staticmethod
    def _position_to_coordinates(position: int) -> tuple:
        """
        Converts the checkers position into coordinates
        :param position: The position in checkers notation
        :return: The X and Y coordinates
        """

        # Round up the y position
        y: int = 9 - math.ceil(position / 4)

        y_mod: int = y % 2
        mod: int = (position % 4)

        if mod != 0:
            x: int = 2 * mod + y_mod
        else:
            y -= 1
            x: int = 8 - y_mod

        # convert the number to a char
        x: str = str(chr(x + 64))
        return x, str(y)
