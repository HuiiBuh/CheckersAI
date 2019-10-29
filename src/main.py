import sys

from play import play_game
from difficulty.Random import Random
from setup import select_difficulty, select_order

# difficulty: int = select_difficulty()
# order: int = select_order()

difficulty: int = 0
order: int = 1

if int(difficulty) == 0:
    random_game: Random = Random(3 - order)
    play_game(random_game, order)
