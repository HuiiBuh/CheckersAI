import multiprocessing
from multiprocessing import Process

import pytest
from aiohttp import ClientSession
from time import sleep

from api.manual_start import manual_start_app
from conftest import TestData


class TestApi:
    api_instance: Process = None

    base_url = 'http://0.0.0.0:1234/'

    @classmethod
    def setup_class(cls):
        mp_context: multiprocessing = multiprocessing.get_context('spawn')

        kwargs = {'location': 'api.main:app', 'reload': False}
        cls.api_instance = mp_context.Process(target=manual_start_app, kwargs=kwargs)
        cls.api_instance.start()
        sleep(5)

    @pytest.mark.asyncio
    async def test_create_board(self, timeout):
        async with ClientSession(timeout=timeout) as session:
            # new game
            url = f'{self.base_url}game?difficulty={TestData.difficulty}&player_first=true'
            async with session.put(url, headers=TestData.headers) as resp:
                j = await resp.json()
                assert isinstance(j, dict)
                assert resp.status == 201

                # get board
            async with session.get(f"{self.base_url}game", headers=TestData.headers) as resp:
                j = await resp.json()
                assert isinstance(j, dict)
                assert resp.status == 200

    @pytest.mark.asyncio
    async def test_invalid_move(self, timeout):
        async with ClientSession(timeout=timeout) as session:
            # new game
            url = f'{self.base_url}game?difficulty={TestData.difficulty}&player_first=true'
            async with session.put(url, headers=TestData.headers) as _:
                pass

                # make a invalid move
            async with session.post(f"{self.base_url}game/move", headers=TestData.headers,
                                    json=TestData.invalid_move) as resp:
                j = await resp.json()
                assert isinstance(j, dict)
                assert resp.status == 418

    @pytest.mark.asyncio
    async def test_valid_move(self, timeout):
        async with ClientSession(timeout=timeout) as session:
            # new game
            url = f'{self.base_url}game?difficulty={TestData.difficulty}&player_first=true'
            async with session.put(url, headers=TestData.headers) as _:
                pass

                # make a valid move
            async with session.post(f"{self.base_url}game/move", headers=TestData.headers,
                                    json=TestData.valid_move) as resp:
                j = await resp.json()
                assert isinstance(j, dict)
                assert resp.status == 200

    @pytest.mark.asyncio
    async def test_delete_game(self, timeout):
        async with ClientSession(timeout=timeout) as session:
            # new game
            url = f'{self.base_url}game?difficulty={TestData.difficulty}&player_first=true'
            async with session.put(url, headers=TestData.headers) as _:
                pass

                # delete game
            async with session.delete(f"{self.base_url}game", headers=TestData.headers) as resp:
                j = await resp.json()
                assert not j
                assert resp.status == 200

    @pytest.mark.asyncio
    async def test_calc_next_move(self, timeout):
        async with ClientSession(timeout=timeout) as session:
            # new game
            url = f'{self.base_url}game?difficulty={TestData.difficulty}&player_first=false'
            async with session.put(url, headers=TestData.headers) as _:
                pass

                # calculate next move
            async with session.get(f"{self.base_url}game/move", headers=TestData.headers) as resp:
                j = await resp.json()
                assert isinstance(j, dict)
                assert resp.status == 200

    @classmethod
    def teardown_class(cls):
        cls.api_instance.terminate()
