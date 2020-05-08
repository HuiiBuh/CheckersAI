import json
from typing import List

from checkers.piece import Piece

from game import MinMax


def export_game():
    monte_carlo_game = MinMax(1, 5)
    monte_carlo_game.move(9, 14)

    piece_list: List[Piece] = monte_carlo_game._game.board.pieces

    dict_list = []
    for piece in piece_list:
        dict_list.append({
            'position': piece.position,
            'player': piece.player,
            'king': piece.king,
        })

    with open('../src/test/one_move_piece_list.json', 'w') as file:
        file.write(json.dumps(dict_list))
        file.close()


if __name__ == '__main__':
    export_game()
