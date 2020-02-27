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
        :return: None
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

    @abstractmethod
    def make_next_move(self):
        """
        Has to be overwritten
        :return: None
        """
        raise NotImplementedError("This method has to be overwritten")
