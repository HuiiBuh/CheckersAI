import asyncio
from typing import List

from aiohttp import ClientSession

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

difficulty = 4


async def make_requests():
    async with ClientSession() as session:
        # new game
        async with session.put(f'http://0.0.0.0:8000/game?difficulty={difficulty}&first=true', headers=headers) as resp:
            j = await resp.json()
            assert isinstance(j, dict)
            assert resp.status == 200

        # get board
        async with session.get("http://0.0.0.0:8000/game", headers=headers) as resp:
            j = await resp.json()
            assert isinstance(j, dict)
            assert resp.status == 200

        # delete game
        async with session.delete("http://0.0.0.0:8000/game", headers=headers) as resp:
            j = await resp.json()
            assert not j
            assert resp.status == 200

        # new game
        async with session.put(f'http://0.0.0.0:8000/game?difficulty={difficulty}&first=true', headers=headers) as resp:
            j = await resp.json()
            assert isinstance(j, dict)
            assert resp.status == 200

        # make a invalid move
        async with session.post("http://0.0.0.0:8000/game/move", headers=headers, json=invalid_move) as resp:
            j = await resp.json()
            assert isinstance(j, dict)
            assert resp.status == 418

        # make a valid move
        async with session.post("http://0.0.0.0:8000/game/move", headers=headers, json=valid_move) as resp:
            j = await resp.json()
            assert isinstance(j, dict)
            assert resp.status == 200

        # send pieces list
        async with session.post("http://0.0.0.0:8000/game/pieces", headers=headers, json=pieces) as resp:
            j = await resp.json()
            assert isinstance(j, List)
            assert resp.status == 200


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(make_requests())
