from time import sleep

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
            start_position: tuple = (int(input("X Start: ")), int(input("Y Start: ")))
            end_position: tuple = (int(input("X End: ")), int(input("Y End: ")))
            game.move(start_position, end_position)

    winner = game.game.get_winner()
    print(f"The winner is player {winner}.")
