from game import MinMax
from game.setup import select_difficulty, select_order

difficulty: int = select_difficulty()
order: int = select_order()

min_max_game = MinMax(3 - order, branch_depth=difficulty)
min_max_game.play_game()
