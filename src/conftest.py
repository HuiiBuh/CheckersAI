import json
from typing import List

import pytest
from aiohttp import ClientTimeout


@pytest.fixture()
def timeout():
    return ClientTimeout(total=(60 * 9))


@pytest.fixture()
def valid_move_pieces():
    with open('one_move_piece_list.json') as file:
        return json.load(file)


class TestData:
    difficulty = 4

    headers: dict = {
        'X-authentication-token': '123456789'
    }

    invalid_move: dict = {
        'origin': 1,
        'target': 1
    }

    valid_move: dict = {
        'origin': 9,
        'target': 14
    }

    pieces: List[dict] = [
        {
            'position': 1,
            'player': 1,
            'king': True
        }, {
            'position': 2,
            'player': 2,
            'king': False
        }
    ]
