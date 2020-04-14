import copy
import random
import time
from sys import maxsize
from typing import Tuple, List, Optional

from checkers.game import Game

from difficulty.algorithm.Opponent import Opponent


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

    def make_next_move(self):
        """
        Make a move based on the min max algorithm
        :return: None
        """

        # Check if it is the turn of the computer
        if self.game.whose_turn() is not self.player or self.game.is_over():
            return

        start_time = time.time()

        score, move = self._start_min_max()

        print("")
        print(f"Score: {score}")
        print(f"Move: {move}")
        print(f"Time: {time.time() - start_time}")
        try:
            self.game.move(move)
        except:
            self.make_next_move()

    def _start_min_max(self) -> Tuple[int, Tuple[int, int]]:

        score, move = self._min_max(game=self.game, maximize_score=True)

        # Return the best move
        return score, move

    def _min_max(self, game: Game, maximize_score: bool, alpha=MinMaxWeight.LOSE, beta=MinMaxWeight.WIN,
                 depth=0) -> List[Optional[int]]:
        """
        Calculate the min max
        :param depth: The current depth of the branch
        :return:
        """

        # Check if the game is over
        if game.is_over():
            winner = game.get_winner()
            if winner == self.player:
                return [MinMaxWeight.WIN, None]
            return [MinMaxWeight.LOSE, None]

        # Check if the max depth is reached
        if depth >= self.branch_depth:
            return [self.evaluate_path(game), None]

        # Get the smallest/largest number to initialize the var
        best_score: float = MinMaxWeight.LOSE if maximize_score else MinMaxWeight.WIN
        best_move = None

        possible_moves = game.get_possible_moves()
        # Shuffle the moves
        possible_moves = random.sample(possible_moves, len(possible_moves))

        # Iterate through the moves and recursively find the best
        for move in possible_moves:
            updated_game = copy.deepcopy(game)
            updated_game.move(move)
            returned_best_score, _ = self._min_max(updated_game, not maximize_score,
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

        return [best_score, best_move]

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

    @staticmethod
    def get_active_pieces(game: Game) -> list:
        """
        Get the active pieces of a game
        :param game: The Game
        :return: A list of still available pieces
        """

        piece_list: list = []
        for piece in game.board.pieces:
            if not piece.captured:
                piece_list.append(piece)

        return piece_list
