from typing import Optional

from fastapi import APIRouter, HTTPException

from api.endpoints.models import Move
from game import MinMaxMP

game: Optional[MinMaxMP] = None

router = APIRouter()


@router.put("/game")
async def new_game(difficulty: int, first: bool = False):
    player = 1 if first else 2

    global game
    game = MinMaxMP(player, difficulty)

    yield game.game.board.position_layout

    game.make_next_move()


@router.get("/game")
async def get_board():
    if not game:
        raise HTTPException(404, {'error': 'You have to create a game first'})

    return game.game.board.position_layout


@router.delete("/game")
async def delete_game():
    global game

    if not game:
        raise HTTPException(404, {'error': 'You have to create a game first'})

    game = None


@router.post("/game/move")
async def read_user(move: Move):
    if not game:
        raise HTTPException(404, {'error': 'You have to create a game first'})

    # Make the proposed move
    try:
        game.game.move([move.origin, move.target])
    except ValueError:
        raise HTTPException(418, {'error': 'The move you provided is not allowed'})

    yield game.game.board.position_layout

    # Calculate the move
    game.make_next_move()
