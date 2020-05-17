from typing import Any, Dict, Optional, Tuple, List

from sys import maxsize

from .MinMaxMP import MinMaxMP
from .MonteCarloMP import MonteCarloMP


class MonteCarloMinMax(MinMaxMP, MonteCarloMP):

    def __init__(self, player: int, difficulty: int):
        super().__init__(player, difficulty)

    def calculate_next_move(self) -> Optional[Dict[str, Any]]:
        min_max_move_list: List[Tuple[float, Optional[int]]] = self._start_min_max()
        monte_carlo_move_list: Optional[List[Dict[str, Any]]] = self._start_monte_carlo()

        if not min_max_move_list and not monte_carlo_move_list:
            return None

        # Create the list with the best moves
        best_score = -maxsize

        # A list of the best moves the minmax search has found

        best_min_max_carlo_moves: List[Dict[str, Any]] = []
        for result in min_max_move_list:
            if result[0] > best_score:
                best_score = result[0]

                best_min_max_carlo_moves = [{
                    "min_max_score": result[0],
                    "move": result[1],
                    "monte_carlo_score": -maxsize
                }]
            elif result[0] == best_score:
                best_min_max_carlo_moves.append({
                    "min_max_score": result[0],
                    "move": result[1],
                    "monte_carlo_score": -maxsize
                })

        for carlo_move in monte_carlo_move_list:
            for min_max_move in best_min_max_carlo_moves:

                if min_max_move["move"] == carlo_move["move"]:
                    min_max_move["monte_carlo_score"] = carlo_move["score"]

        best_score = -maxsize
        best_move: Optional[Dict[str, Any]] = None
        for carlo_min_move in best_min_max_carlo_moves:

            if carlo_min_move["monte_carlo_score"] > best_score:
                best_score = carlo_min_move["monte_carlo_score"]
                best_move = carlo_min_move

        return best_move
