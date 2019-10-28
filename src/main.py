from play import play_game
from difficulty.RandomGame import RandomGame
from setup import select_difficulty, select_order

difficulty: int = select_difficulty()
order: int = select_order()

if int(difficulty) == 0:
    random_game: RandomGame = RandomGame(3 - order)
    play_game(random_game, order)
