import copy
from sys import maxsize

import time
from checkers.game import Game

from difficulty.Opponent import Opponent


class MinMax(Opponent):
    def __init__(self, player: int, branch_depth: int):
        """
        Create a new MinMax Opponent
        :param player: The player number
        :param branch_depth: The depth of the min max calculation
        """
        super().__init__(player)
        self.branch_depth: int = branch_depth

    def _make_next_move(self):
        """
        Make a move based on the min max algorithm
        :return: None
        """

        # Check if it is the turn of the computer
        if self.game.whose_turn() is not self.player:
            return

        game_copy: Game = copy.deepcopy(self.game)

        start = time.time()
        score, move = self._min_max(game_copy, maximize_score=True)
        print(time.time() - start)

        print(move)
        print(f"{self._position_to_coordinates(move[0])}/{self._position_to_coordinates(move[1])}")
        self.game.move(move)

    def _min_max(self, game: Game, maximize_score: bool, depth=0):
        """
        Calculate the min max
        :param depth: The current depth of the branch
        :return:
        """

        # Check if the game is over
        if game.is_over():
            winner = game.get_winner()
            if winner == self.player:
                return MinMaxWeight.WINN, None
            return MinMaxWeight.LOSE, None

        # Check if the max depth is reached
        if depth >= self.branch_depth:
            return self.evaluate_path(game), None

        # Get the smallest/largest number to initialize the var
        best_score: float = MinMaxWeight.LOSE if maximize_score else MinMaxWeight.WINN

        move = None
        # Iterate through the moves and recursively find the best

        moves = game.get_possible_moves()
        for move in moves:
            updated_game = copy.deepcopy(game)
            updated_game.move(move)
            score, _ = self._min_max(updated_game, not maximize_score, depth + 1)
            if maximize_score:
                best_score = max(score, best_score)
            else:
                best_score = min(score, best_score)

        return best_score, move

    def evaluate_path(self, game: Game):
        """
        Evaluates the score of the computer and the human at a certain point of the game
        :param game: The game that is supposed to be evaluated
        :return: The score (positive if the computer is better and visa versa)
        """

        computer_score = 0
        human_score = 0

        # For every piece in the ame
        for piece in game.board.pieces:
            # Check if the piece is still available
            if not piece.captured:
                # Get the owner of the piece
                if piece.player is self.player:
                    # Get the type of the piece and add a value
                    if piece.king:
                        computer_score += MinMaxWeight.KING
                    else:
                        computer_score += MinMaxWeight.PICE
                else:
                    # Get the type of the piece and add a value
                    if piece.king:
                        human_score += MinMaxWeight.KING
                    else:
                        human_score += MinMaxWeight.PICE

        return computer_score - human_score

    @staticmethod
    def get_active_pieces(game: Game) -> list:
        """
        Get the active pieces of a game #TODO in library
        :param game: The Game
        :return: A list of still available pieces
        """

        piece_list: list = []
        for piece in game.board.pieces:
            if not piece.captured:
                piece_list.append(piece)

        return piece_list


class MinMaxWeight:
    WINN = maxsize
    LOSE = -maxsize
    PICE = 1
    KING = 1.5
