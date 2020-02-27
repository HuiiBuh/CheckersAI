import copy
import random
import time
from sys import maxsize

from checkers.game import Game

from difficulty.algorithm.Opponent import Opponent


class MonteCarlo(Opponent):

    def make_next_move(self):
        move_list = self.game.board.get_possible_moves()

        s = time.time()

        move_score_list = []
        for move in move_list:
            move_score_list.append(self._tree_search(move, self.game))

        best_move_score = {"move": None, "score": -maxsize}
        for move_score in move_score_list:

            if move_score["score"] > best_move_score["score"]:
                best_move_score = move_score

        print(time.time() - s)

    def _tree_search(self, old_move, game: Game) -> dict:
        updated_game = copy.deepcopy(game)
        updated_game.move(old_move)

        move_list = updated_game.board.get_possible_moves()
        score = 0
        for move in move_list:
            score += self._calculate_to_end(move, updated_game)

        return {"move": old_move, "score": score}

    def _calculate_to_end(self, old_move, game):
        updated_game = copy.deepcopy(game)
        m = updated_game.board.get_possible_moves()

        updated_game.move(old_move)

        while not updated_game.is_over():
            possible_moves = updated_game.get_possible_moves()
            move = random.sample(possible_moves, len(possible_moves))[0]

            updated_game.move(move)

        winner = updated_game.get_winner()

        if winner is None:
            return 0

        if winner is self.player:
            return 1

        return -1


c = MonteCarlo(1)
c.make_next_move()
