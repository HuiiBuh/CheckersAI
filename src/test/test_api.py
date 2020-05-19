import multiprocessing
from multiprocessing import Process

import pytest
from time import sleep

from api.manual_start import manual_start_app
from conftest import TestData


class TestApi:
    api_instance: Process = None

    base_url = 'http://0.0.0.0:1234'

    @classmethod
    def setup_class(cls):
        mp_context: multiprocessing = multiprocessing.get_context('spawn')

        kwargs = {'location': 'api.main:app', 'reload': False}
        cls.api_instance = mp_context.Process(target=manual_start_app, kwargs=kwargs)
        cls.api_instance.start()
        sleep(5)

    @pytest.mark.asyncio
    async def test_create_board(self, session):
        # new game
        async with session.put(f'{self.base_url}/game?difficulty={TestData.difficulty}&player_first=true') as resp:
            j = await resp.json()
            game_key = j['game_key']
            assert isinstance(j, dict)
            assert resp.status == 201

            # get board
        async with session.get(f"{self.base_url}/game/{game_key}") as resp:
            j = await resp.json()
            assert isinstance(j, dict)
            assert resp.status == 200

    @pytest.mark.asyncio
    async def test_invalid_move(self, session):
        # new game
        async with session.put(f'{self.base_url}/game?difficulty={TestData.difficulty}&player_first=true') as resp:
            j = await resp.json()
            game_key = j['game_key']

            # make a invalid move
        async with session.post(f"{self.base_url}/game/{game_key}/move", json=TestData.invalid_move) as resp:
            j = await resp.json()
            assert isinstance(j, dict)
            assert resp.status == 418

    @pytest.mark.asyncio
    async def test_valid_move(self, session):
        # new game
        async with session.put(f'{self.base_url}/game?difficulty={TestData.difficulty}&player_first=true') as resp:
            j = await resp.json()
            game_key = j['game_key']

            # make a valid move
        async with session.post(f"{self.base_url}/game/{game_key}/move", json=TestData.valid_move) as resp:
            j = await resp.json()
            assert isinstance(j, dict)
            assert resp.status == 200

    @pytest.mark.asyncio
    async def test_delete_game(self, session):
        # new game
        async with session.put(f'{self.base_url}/game?difficulty={TestData.difficulty}&player_first=true') as resp:
            j = await resp.json()
            game_key = j['game_key']

            # delete game
        async with session.delete(f"{self.base_url}/game/{game_key}") as resp:
            j = await resp.json()
            assert not j
            assert resp.status == 200

    @pytest.mark.asyncio
    async def test_calc_next_move(self, session):
        # new game
        async with session.put(f'{self.base_url}/game?difficulty={TestData.difficulty}&player_first=false') as resp:
            j = await resp.json()
            game_key = j['game_key']

        # calculate next move
        async with session.get(f"{self.base_url}/game/{game_key}/move") as resp:
            move = await resp.json()
            assert isinstance(j, dict)
            assert resp.status == 200

        async with session.post(f"{self.base_url}/game/{game_key}/move", json=move['move']) as resp:
            j = await resp.json()

            assert j
            assert not j['removed_pieces']
            assert not j['new_kings']
            assert resp.status == 200

    @pytest.mark.asyncio
    async def test_hole_game(self, session):
        # new game
        async with session.put(f'{self.base_url}/game?difficulty={TestData.difficulty}&player_first=false') as resp:
            j = await resp.json()
            game_key = j['game_key']

        is_over = False
        while not is_over:
            # calculate next move
            async with session.get(f"{self.base_url}/game/{game_key}/move") as resp:
                assert resp.status == 200
                move = await resp.json()

            async with session.post(f"{self.base_url}/game/{game_key}/move", json=move['move']) as resp:
                assert resp.status == 200
                j = await resp.json()
                is_over = j['game_state']['is_over']

    @classmethod
    def teardown_class(cls):
        cls.api_instance.terminate()
