from difficulty.MinMax import MinMax
from play import play_game
from difficulty.Random import Random

# difficulty: int = select_difficulty()
# order: int = select_order()

difficulty: int = 1
order: int = 1

if difficulty == 0:
    random_game: Random = Random(3 - order)
    play_game(random_game, order)
elif difficulty == 1:
    min_max_game = MinMax(3 - order, branch_depth=4)
    play_game(min_max_game, order)
