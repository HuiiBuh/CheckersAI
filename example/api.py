import asyncio

from aiohttp import ClientSession

headers: dict = {
    'X-authentication-token': '123456789'
}
invalid_move: dict = {
    'origin': 1,
    'target': 1
}

valid_move: dict = {
    'origin': 21,
    'target': 17
}

difficulty = 4


async def make_requests():
    async with ClientSession() as session:
        # new game
        async with session.put(f'http://0.0.0.0:8000/game?difficulty={difficulty}&first=true', headers=headers) as resp:
            print(await resp.json())

        # get game
        async with session.get("http://0.0.0.0:8000/game", headers=headers) as resp:
            print(await resp.json())

        # delete game
        async with session.delete("http://0.0.0.0:8000/game", headers=headers) as resp:
            print(await resp.json())

        # make a invalid move
        async with session.post("http://0.0.0.0:8000/game/move", headers=headers, data=invalid_move) as resp:
            print(await resp.json())

        # make a valid move
        async with session.post("http://0.0.0.0:8000/game/move", headers=headers, data=invalid_move) as resp:
            print(await resp.json())


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(make_requests())
