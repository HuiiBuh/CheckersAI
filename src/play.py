from time import sleep

from Colors import COLOUR
from difficulty import Opponent


def play_game(game: Opponent, player: int) -> None:
    """
    Play the game
    :param game: The game object
    :param player: If the user is player one or two
    :return: None
    """
    game.start()

    while not game.game.is_over():
        sleep(0.1)
        if game.game.whose_turn() == player:

            start_position: str = input("Start: ")
            end_position: str = input("End: ")

            if not (start_position.isdigit() and end_position.isdigit()):
                print(COLOUR.RED + "You can only input numbers" + COLOUR.END)
            else:
                start_position: int = int(start_position)
                end_position: int = int(end_position)

                try:
                    game.move(start_position, end_position)
                except Exception as e:
                    print(COLOUR.RED + str(e) + COLOUR.END + "\n\n")
        else:
            game.make_next_move()

    winner = game.game.get_winner()
    print(COLOUR.GREEN + f"The winner is player {winner}." + COLOUR.END)
