import copy
import random
from typing import Tuple, List, Optional

from checkers.game import Game
from sys import maxsize

from game.algorithm.Opponent import Opponent


class MinMaxWeight:
    WIN = maxsize
    LOSE = -maxsize
    POSITION = .2
    PIECE = 1
    KING = 1.5


class MinMax(Opponent):
    def __init__(self, player: int, branch_depth: int):
        """
        Create a new MinMax Opponent
        :param player: The player number
        :param branch_depth: The depth of the min max calculation
        """

        super().__init__(player)
        self.branch_depth: int = branch_depth

    def calculate_next_move(self) -> Optional[dict]:
        """
        Make a move based on the min max algorithm
        :return: None
        """

        # Check if it is the turn of the computer
        if self.game.whose_turn() is not self.player or self.game.is_over():
            return None

        score, move = self._start_min_max()
        return {'move': move, 'score': score}

    def _start_min_max(self) -> Tuple[float, Optional[int]]:
        """Call the min max calculation"""

        return self._min_max(game=self.game, maximize_score=True)

    def _min_max(self, game: Game,
                 maximize_score: bool,
                 move_list: List[Tuple[int, int]] = None,
                 alpha=MinMaxWeight.LOSE, beta=MinMaxWeight.WIN,
                 depth=0) \
            -> Tuple[float, Optional[int]]:
        """
        Calculate the min max
        :param depth: The current depth of the branch
        :return: The score and the move
        """

        # Check if the game is over
        if game.is_over():
            winner = game.get_winner()
            if winner == self.player:
                return MinMaxWeight.WIN, None
            return MinMaxWeight.LOSE, None

        # Check if the max depth is reached
        if depth >= self.branch_depth:
            return self.evaluate_path(game), None

        if not move_list:
            move_list = game.get_possible_moves()
            random.shuffle(move_list)

        # Get the smallest/largest number to initialize the var
        best_score: float = MinMaxWeight.LOSE if maximize_score else MinMaxWeight.WIN
        best_move = move_list[0]

        # Iterate through the moves and recursively find the best
        for move in move_list:
            updated_game = copy.deepcopy(game)
            updated_game.move(move)
            returned_best_score, _ = MinMax._min_max(self, updated_game, not maximize_score,
                                                     alpha=alpha,
                                                     beta=beta,
                                                     depth=depth + 1)

            if maximize_score and best_score < returned_best_score:
                best_score = returned_best_score
                best_move = move
                alpha = max(alpha, best_score)

                if beta <= alpha:
                    break

            elif not maximize_score and returned_best_score < best_score:
                best_score = returned_best_score
                best_move = move
                beta = min(beta, best_score)

                if beta <= alpha:
                    break

        return best_score, best_move

    def evaluate_path(self, game: Game):
        """
        Evaluates the score of the computer and the human at a certain point of the game
        :param game: The game that is supposed to be evaluated
        :return: The score (positive if the computer is better and visa versa)
        """

        computer_score = 0
        human_score = 0

        # For every piece in the ame
        for piece in self.get_active_pieces(game):

            # Get the owner of the piece
            if piece.player is self.player:
                # Get the type of the piece and add a value
                if piece.king:
                    computer_score += MinMaxWeight.KING
                else:
                    computer_score += MinMaxWeight.PIECE
            else:
                # Get the type of the piece and add a value
                if piece.king:
                    human_score += MinMaxWeight.KING
                else:
                    human_score += MinMaxWeight.PIECE

        return computer_score - human_score
