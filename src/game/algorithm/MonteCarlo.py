import copy
import random
from sys import maxsize

from checkers.game import Game

from game.algorithm.Opponent import Opponent


class MonteCarlo(Opponent):

    def __init__(self, player: int, move_count: int):
        self.move_count: int = move_count
        super().__init__(player)

    def make_next_move(self):

        # Check if it is the turn of the computer
        if self.game.whose_turn() is not self.player or self.game.is_over():
            return

        # Get the possible moves
        move_list: list = self.game.board.get_possible_moves()

        # Get the best score
        move_score_list = []
        for move in move_list:
            move_score = self._tree_search(move, self.game, self.move_count)
            move_score_list.append(move_score)

        best_move_score = {"move": None, "score": -maxsize}
        for move_score in move_score_list:

            if move_score["score"] > best_move_score["score"]:
                best_move_score = move_score

        self.game.move(best_move_score["move"])
        print(best_move_score)

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
