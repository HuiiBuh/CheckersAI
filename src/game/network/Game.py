import itertools
from typing import List

from checkers.game import Game
from checkers.piece import Piece


class NCheckersGame(Game):

    def board_to_matrix(self) -> List[List[int]]:
        """
        Takes the board and transforms it into a matrix
        :return: The matrix
        """

        piece_list: List[Piece] = self.board.pieces

        piece_matrix = self._initialize_matrix()
        for piece in piece_list:
            if not piece.captured:
                position = piece.position
                player = piece.player
                king = int(piece.king)

                piece_matrix[position - 1] = [2 - player, king, abs(1 - player)]

        return piece_matrix

    @staticmethod
    def _initialize_matrix() -> List[List[int]]:
        """
        Create an empty matrix
        :return: The empty matrix
        """

        piece_matrix = []

        for _ in range(32):
            piece_matrix.append([0, 0, 0])

        return piece_matrix

    def board_to_flat_matrix(self):
        matrix = self.board_to_matrix()
        flat_matrix = list(itertools.chain(*matrix))
        return flat_matrix
