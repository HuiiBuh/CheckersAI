import copy
import random
from typing import Optional, Any, Dict, List

from checkers.game import Game
from sys import maxsize

from game.algorithm.Opponent import Opponent


class MonteCarlo(Opponent):

    def __init__(self, player: int, path_count: int):
        """
        Create a new MonteCarlo game
        :param player: Which player
        :param path_count: How many path traces
        """

        super().__init__(player, path_count)
        self.move_count: int = path_count

    def calculate_next_move(self) -> Optional[dict]:
        move_score_list: List[Dict[str, Any]] = self._start_monte_carlo()

        if not move_score_list:
            return None

        best_move_score = {"move": None, "score": -maxsize}

        for move_score in move_score_list:
            if move_score["score"] > best_move_score["score"]:
                best_move_score = move_score

        return best_move_score

    def _start_monte_carlo(self) -> Optional[List[Dict[str, Any]]]:

        # Check if it is the turn of the computer
        if self._game.whose_turn() is not self.player or self._game.is_over():
            return None

        # Get the possible moves
        move_list: list = self._game.board.get_possible_moves()

        # Get the best score
        move_score_list: List[Dict[str, Any]] = []
        for move in move_list:
            move_score = self._tree_search(move, self._game, self.move_count)
            move_score_list.append(move_score)

        return move_score_list

    def _tree_search(self, old_move: list, game: Game, move_count: int) -> dict:

        game = copy.deepcopy(game)
        game.move(old_move)

        # Check if the game has ended
        if game.is_over():
            if game.get_winner() is None:
                return {"move": old_move, "score": 0}

            if game.get_winner() == self.player:
                return {"move": old_move, "score": maxsize}

            return {"move": old_move, "score": -maxsize}

        score = 0
        for _ in range(move_count):
            score += self._calculate_to_end(game)

        return {"move": old_move, "score": score}

    def _calculate_to_end(self, game):
        game = copy.deepcopy(game)

        while not game.is_over():
            possible_moves = game.get_possible_moves()
            random.shuffle(possible_moves)
            game.move(possible_moves[0])

        if game.get_winner() is None:
            return 0

        if game.get_winner() == self.player:
            return 1

        return -1
