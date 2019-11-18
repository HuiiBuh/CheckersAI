from difficulty.MinMax import MinMax
from difficulty.Random import Random
from play import play_game
from setup import select_difficulty, select_order

difficulty: int = select_difficulty()
order: int = select_order()


if difficulty == 0:
    random_game: Random = Random(3 - order)
    play_game(random_game, order)
elif difficulty > 0:
    min_max_game = MinMax(3 - order, branch_depth=difficulty)
    play_game(min_max_game, order)
