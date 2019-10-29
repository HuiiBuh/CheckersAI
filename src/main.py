from play import play_game
from difficulty.RandomGame import RandomGame
from setup import select_difficulty, select_order

# difficulty: int = select_difficulty()
# order: int = select_order()

difficulty: int = 0
order: int = 1

if int(difficulty) == 0:
    random_game: RandomGame = RandomGame(3 - order)
    # print(random_game._position_to_coordinates(20))
    play_game(random_game, order)
