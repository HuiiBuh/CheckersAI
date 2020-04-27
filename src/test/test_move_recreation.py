from typing import List, Tuple

import pytest

from api.endpoints.models import CheckersPiece
from game import MinMax


def test_one_move_recreation(valid_one_move_pieces):
    min_max = MinMax(1, 1)

    move: List[Tuple[int, int]] = min_max.get_move_by_pieces(valid_one_move_pieces)
    assert move == [[9, 14]]


def test_invalid_one_move_recreation(valid_one_move_pieces):
    valid_one_move_pieces[0].king = True

    min_max = MinMax(1, 1)

    with pytest.raises(ValueError):
        min_max.get_move_by_pieces(valid_one_move_pieces)


def test_load_game():
    min_max = MinMax(1, 1)

    piece_1 = CheckersPiece(position=18, player=1, king=True)
    piece_2 = CheckersPiece(position=22, player=2, king=True)

    min_max.load_game([piece_1, piece_2])

    moves = min_max.game.get_possible_moves()[0]
    min_max.move(*moves)

    assert min_max.game.is_over()


def test_multi_move_recreation(valid_multi_move_pieces):
    min_max = MinMax(1, 1)

    piece_1 = CheckersPiece(position=29, player=1, king=True)
    piece_2 = CheckersPiece(position=25, player=2, king=True)
    piece_3 = CheckersPiece(position=18, player=2, king=True)
    piece_4 = CheckersPiece(position=11, player=2, king=True)

    min_max.load_game([piece_1, piece_2, piece_3, piece_4])

    move: List[Tuple[int, int]] = min_max.get_move_by_pieces(valid_multi_move_pieces)
    assert move == [[29, 22], [22, 15], [15, 8]]
