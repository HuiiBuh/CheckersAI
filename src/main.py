from difficulty.MinMax import MinMax
from difficulty.Random import Random
from play import play_game

# difficulty: int = select_difficulty()
# order: int = select_order()

difficulty: int = 1
order: int = 1

if difficulty == 0:
    random_game: Random = Random(order)
    play_game(random_game, order)
elif difficulty == 1:
    min_max_game = MinMax(order, branch_depth=8)
    play_game(min_max_game, 3 - order)
