from typing import Optional, List

from fastapi import APIRouter, HTTPException
from fastapi.websockets import WebSocket

from api.endpoints.models import Move, CheckersPiece
from game import MinMaxMP

game: Optional[MinMaxMP] = None

router = APIRouter()


# TODO get the hole thing to work with yield


@router.put("/game")
async def new_game(difficulty: int, first: bool = False):
    """
    Create a new game
    :param difficulty: The difficulty of the game
    :param first: Does the player want to be first
    """
    player = 1 if first else 2

    global game
    game = MinMaxMP(player, difficulty)

    return game.game.board.position_layout


@router.get("/game")
async def get_board():
    """Get the current game board"""

    if not game:
        raise HTTPException(404, {'error': 'You have to create a game first'})

    return game.game.board.position_layout


@router.delete("/game")
async def delete_game():
    """Delete the game"""

    global game

    if not game:
        raise HTTPException(404, {'error': 'You have to create a game first'})

    game = None


@router.post('/game/pieces')
async def update_board(piece_list: List[CheckersPiece]):
    """
    Update the game with a list of pieces. After this a try to reconstruct the move is made
    :param piece_list: A list of pieces which represent the game
    """

    # TODO update the game with the piece list
    return piece_list


@router.post("/game/move")
async def read_user(move: Move):
    """
    Make a move
    :param move: A valid move
    """

    if not game:
        raise HTTPException(404, {'error': 'You have to create a game first'})

    try:
        game.game.move([move.origin, move.target])
    except ValueError:
        raise HTTPException(418, {'error': 'The move you provided is not allowed'})

    return game.game.board.position_layout


@router.websocket("/current-game")
async def current_game(websocket: WebSocket):
    """
    Subscribe to the current game to get updates
    """

    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")

    # TODO make the websocket emit the new board every time something happens
