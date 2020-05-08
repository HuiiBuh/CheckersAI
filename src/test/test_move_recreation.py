from copy import deepcopy
from typing import List, Tuple

import pytest
from checkers.game import Game

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

    moves = min_max._game.get_possible_moves()[0]
    min_max.move(*moves)

    assert min_max._game.is_over()


def test_multi_move_recreation(valid_multi_move_pieces):
    min_max = MinMax(1, 1)

    piece_1 = CheckersPiece(position=29, player=1, king=True)
    piece_2 = CheckersPiece(position=25, player=2, king=True)
    piece_3 = CheckersPiece(position=18, player=2, king=True)
    piece_4 = CheckersPiece(position=11, player=2, king=True)

    min_max.load_game([piece_1, piece_2, piece_3, piece_4])

    move: List[Tuple[int, int]] = min_max.get_move_by_pieces(valid_multi_move_pieces)
    assert move == [[29, 22], [22, 15], [15, 8]]


def test_piece_removal(valid_multi_move_pieces):
    min_max = MinMax(1, 1)

    piece_1 = CheckersPiece(position=29, player=1, king=True)
    piece_2 = CheckersPiece(position=25, player=2, king=True)
    piece_3 = CheckersPiece(position=18, player=2, king=True)
    piece_4 = CheckersPiece(position=11, player=2, king=True)

    min_max.load_game([piece_1, piece_2, piece_3, piece_4])

    old_game: Game = deepcopy(min_max._game)
    move_list = min_max.get_move_by_pieces(valid_multi_move_pieces)

    for move in move_list:
        min_max.move(*move)

    removed_pieces = min_max.get_removed_pieces(old_game, min_max._game, min_max._game.whose_turn())
    assert removed_pieces == [25, 18, 11]


def test_new_king():
    min_max = MinMax(2, 1)

    piece_1 = CheckersPiece(position=6, player=2, king=False)
    piece_2 = CheckersPiece(position=8, player=1, king=False)

    min_max.load_game([piece_1, piece_2])

    min_max.move(8, 11)

    old_game: Game = deepcopy(min_max._game)
    min_max.move(6, 1)

    king_pieces = min_max.get_new_kings(old_game, min_max._game, old_game.whose_turn(), (6, 1))
    assert king_pieces == [1]
