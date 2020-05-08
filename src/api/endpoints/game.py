from copy import deepcopy
from typing import Optional, List, Tuple, Dict, Any

import time
from checkers.piece import Piece
from fastapi import APIRouter, HTTPException, status, Response

from api.endpoints.GameHolder import GameHolder
from api.endpoints.models import Move, CheckersPiece
from game import MinMaxMP
from game.algorithm.MonteCarloMinMax import MonteCarloMinMax
from game.algorithm.Opponent import Opponent

router = APIRouter()
game_holder = GameHolder()


@router.get('/ping')
async def ping_pong(response: Response):
    response.headers["X-Send-Time"] = str(time.time())
    return {}


@router.put("/game/load", status_code=status.HTTP_201_CREATED)
async def load_game(piece_list: List[CheckersPiece], difficulty: int, player_first: bool = False):
    """ Load the game """
    player = 2 if player_first else 1
    game_key = game_holder.add_game(MinMaxMP(player, difficulty))
    game_holder[game_key].load_game(piece_list)

    return {'game_key': game_key}


@router.put("/game", status_code=status.HTTP_201_CREATED)
async def new_game(difficulty: int, player_first: bool = False):
    """
    Create a new game
    :param difficulty: The difficulty of the game
    :param player_first: Does the player want to be first
    """
    player = 2 if player_first else 1

    game_key = game_holder.add_game(MonteCarloMinMax(player, difficulty))

    return {'game_key': game_key}


@router.get("/game/{game_key}")
async def get_board(game_key: str):
    """Get the current game board"""

    game_instance = game_holder[game_key]

    if not game_instance:
        raise HTTPException(404, 'Your game key is invalid.')

    return get_game_state(game_instance)


@router.delete("/game/{game_key}")
async def delete_game(game_key: str):
    """Delete the game"""

    if not game_holder[game_key]:
        raise HTTPException(404, 'Your game key is invalid.')

    del game_holder[game_key]


@router.post('/game/{game_key}/pieces-to-move')
async def update_board(game_key: str, piece_list: List[CheckersPiece]):
    """
    Update the game with a list of pieces. After this a try to reconstruct the move is made
    :param game_key: A game key
    :param piece_list: A list of pieces which represent the game
    """

    game_instance = game_holder[game_key]

    if not game_instance:
        raise HTTPException(404, 'Your game key is invalid.')

    try:
        move_list: List[Tuple[int, int]] = game_instance.get_move_by_pieces(piece_list)
    except ValueError as e:
        raise HTTPException(400, str(e))

    return_move_list = []
    for move in move_list:
        return_move_list.append({
            'origin': move[0],
            'target': move[1]
        })

    return {'move_list': return_move_list}


@router.get('/game/{game_key}/move')
async def calculate_move(game_key: str):
    """Calculate the next move"""

    game_instance = game_holder[game_key]

    if not game_instance:
        raise HTTPException(404, 'Your game key is invalid.')

    proposed_move = game_instance.calculate_next_move()

    if not proposed_move:
        raise HTTPException(400, 'It is not the turn of the computer or the game is over')

    return {
        'move': {
            'origin': proposed_move['move'][0],
            'target': proposed_move['move'][1]
        },
        'score': proposed_move['min_max_score'] + proposed_move['monte_carlo_score']
    }


@router.post("/game/{game_key}/move")
async def make_move(game_key: str, move: Move):
    """
    Make a move
    :param game_key: The game key
    :param move: A valid move
    """

    game_instance = game_holder[game_key]

    # Copy the game
    old_game = deepcopy(game_instance.game)
    player = game_instance.game.whose_turn()

    if not game_instance:
        raise HTTPException(404, 'Your game key is invalid.')

    try:
        game_instance.game.move([move.origin, move.target])
    except ValueError:
        raise HTTPException(418, 'The move you provided is not allowed')

    # Get the removed pieces
    removed_pieces = game_instance.get_removed_pieces(old_game, game_instance.game, 1 - player)

    # Get new kings
    new_kings = game_instance.get_new_kings(old_game, game_instance.game, player, (move.origin, move.target))

    return {
        'removed_pieces': removed_pieces,
        'new_kings': new_kings
    }


def get_game_state(opponent: Opponent) -> Dict[str, Any]:
    """Get the game state as dict"""

    piece_list: List[Piece] = opponent.get_active_pieces(opponent.game)

    update_piece_list = []
    for piece in piece_list:
        update_piece_list.append(CheckersPiece(position=piece.position, king=piece.king, player=piece.player))

    player_turn: int = opponent._game.whose_turn()
    winner: Optional[int] = opponent._game.get_winner()
    is_over: bool = opponent._game.is_over()

    return {
        'board': update_piece_list,
        'player_turn': player_turn,
        'winner': winner,
        'is_over': is_over
    }
