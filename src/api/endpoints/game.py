from typing import Optional, List, Tuple

from checkers.game import Game
from fastapi import APIRouter, HTTPException, status

from api.endpoints.models import Move, CheckersPiece
from game import MinMaxMP

game: Optional[MinMaxMP] = None

router = APIRouter()


@router.put("/game", status_code=status.HTTP_201_CREATED)
async def new_game(difficulty: int, player_first: bool = False):
    """
    Create a new game
    :param difficulty: The difficulty of the game
    :param player_first: Does the player want to be first
    """
    player = 2 if player_first else 1

    global game
    game = MinMaxMP(player, difficulty)

    return get_game_state(game.game)


@router.get("/game")
async def get_board():
    """Get the current game board"""

    if not game:
        raise HTTPException(404, 'You have to create a game first')

    return get_game_state(game.game)


@router.delete("/game")
async def delete_game():
    """Delete the game"""
    global game
    game = None


@router.post('/game/pieces')
async def update_board(piece_list: List[CheckersPiece]):
    """
    Update the game with a list of pieces. After this a try to reconstruct the move is made
    :param piece_list: A list of pieces which represent the game
    """

    try:
        move_list: List[Tuple[int, int]] = game.get_move_by_pieces(piece_list)
    except ValueError as e:
        raise HTTPException(400, str(e))

    for move in move_list:
        game.move(*move)

    return get_game_state(game.game)


@router.get('/game/move')
async def calculate_move():
    """Calculate the next move"""

    if not game:
        raise HTTPException(404, 'You have to create a game first')

    proposed_move = game.calculate_next_move()

    if not proposed_move:
        raise HTTPException(400, 'It is not the turn of the computer')

    return {
        'move': {
            'origin': proposed_move['move'][0],
            'target': proposed_move['move'][1]
        },
        'score': proposed_move['score']
    }


@router.post("/game/move")
async def make_move(move: Move):
    """
    Make a move
    :param move: A valid move
    """

    if not game:
        raise HTTPException(404, 'You have to create a game first')

    try:
        game.game.move([move.origin, move.target])
    except ValueError:
        raise HTTPException(418, 'The move you provided is not allowed')

    return get_game_state(game.game)


def get_game_state(internal_game: Game) -> dict:
    """Get the game state as dict"""

    # TODO something more meaningful for this please
    board: dict = internal_game.board.position_layout
    player_turn: int = internal_game.whose_turn()
    winner: Optional[int] = internal_game.get_winner()
    is_over: bool = internal_game.is_over()

    return {
        'board': board,
        'player_turn': player_turn,
        'winner': winner,
        'is_over': is_over
    }
