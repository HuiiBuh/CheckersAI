import json
from typing import List

import pytest
from aiohttp import ClientTimeout, ClientSession

from api.endpoints.models import CheckersPiece


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


@pytest.fixture()
async def session():
    timeout = ClientTimeout(total=(10))
    session = ClientSession(timeout=timeout, headers=TestData.headers)

    yield session

    await session.close()


def load_file(filename: str):
    try:
        with open(f'{filename}') as file:
            j = json.load(file)
    except FileNotFoundError:
        try:
            with open(f'test/{filename}') as file:
                j = json.load(file)
        except FileNotFoundError:
            with open(f'src/test/{filename}') as file:
                j = json.load(file)
    return j


@pytest.fixture()
def valid_one_move_pieces():
    one_move_list: List[CheckersPiece] = []
    move_json = load_file('one_move_piece_list.json')

    for piece in move_json:
        one_move_list.append(CheckersPiece(**piece))

    return one_move_list


@pytest.fixture()
def valid_multi_move_pieces():
    _multi_move_list: List[CheckersPiece] = []
    move_json = load_file('multi_move_piece_list.json')

    for piece in move_json:
        _multi_move_list.append(CheckersPiece(**piece))

    return _multi_move_list
