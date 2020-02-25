from difficulty.MinMax import MinMax
from difficulty.Random import Random
from setup import select_difficulty, select_order

difficulty: int = select_difficulty()
order: int = select_order()

if difficulty == 0:
    random_game: Random = Random(3 - order)
    random_game.play_game()

elif difficulty > 0:
    min_max_game = MinMax(3 - order, branch_depth=difficulty)
    min_max_game.play_game()
