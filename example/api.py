import asyncio
from typing import List

from aiohttp import ClientSession, ClientTimeout

headers: dict = {
    'X-authentication-token': 'a_random_token_please'
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
    timeout = ClientTimeout(total=(60 * 9))

    async with ClientSession(timeout=timeout) as session:
        # new game
        async with session.put(f'http://0.0.0.0:1234/game?difficulty={difficulty}&player_first=true',
                               headers=headers) as resp:
            j = await resp.json()
            assert isinstance(j, dict)
            assert resp.status == 201
            key = j['game_key']

        # get board
        async with session.get(f"http://0.0.0.0:1234/game/{key}", headers=headers) as resp:
            j = await resp.json()
            assert isinstance(j, dict)
            assert resp.status == 200

        # make a invalid move
        async with session.post(f"http://0.0.0.0:1234/game/{key}/move", headers=headers, json=invalid_move) as resp:
            j = await resp.json()
            assert isinstance(j, dict)
            assert resp.status == 418

        # make a valid move
        async with session.post(f"http://0.0.0.0:1234/game/{key}/move", headers=headers, json=valid_move) as resp:
            j = await resp.json()
            assert isinstance(j, dict)
            assert resp.status == 200

        # calculate next move
        async with session.get(f"http://0.0.0.0:1234/game/{key}/move", headers=headers) as resp:
            j = await resp.json()
            assert isinstance(j, dict)
            assert resp.status == 200

        # delete game
        async with session.delete(f"http://0.0.0.0:1234/game/{key}", headers=headers) as resp:
            j = await resp.json()
            assert not j
            assert resp.status == 200

        # new game
        async with session.put(f'http://0.0.0.0:1234/game?difficulty={difficulty}', headers=headers) as resp:
            j = await resp.json()
            assert isinstance(j, dict)
            assert resp.status == 201
            new_key = j['game_key']

        # calculate next move
        async with session.get(f"http://0.0.0.0:1234/game/{new_key}/move", headers=headers) as resp:
            j = await resp.json()
            assert isinstance(j, dict)
            assert resp.status == 200


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(make_requests())
