from abc import ABC, abstractmethod
from copy import deepcopy
from typing import Optional, List, Dict, Tuple

from checkers.game import Game
from checkers.piece import Piece
from time import sleep

from game.Colors import COLOUR


class CheckersPiece:
    position: int
    player: int
    king: bool


class Opponent(ABC):
    def __init__(self, player: int):
        """
        Generate a new Random game
        :param player: The player of the RandomGame (1 or 2)
        """

        self.player = player
        self.game = Game()

    def __repr__(self) -> Game:
        """
        Returns the game
        :return: The currently playing game
        """

        return self.game

    def __history__(self) -> list:
        """
        Returns the history of the game
        :return: List of moves that happened in the game
        """

        return self.game.moves

    def play_game(self) -> None:
        """
        Play the game with actual player input
        :return: None
        """

        while not self.game.is_over():
            sleep(0.1)
            if self.game.whose_turn() != self.player:

                start_position: str = input("Start: ")
                end_position: str = input("End: ")

                if not (start_position.isdigit() and end_position.isdigit()):
                    print(COLOUR.RED + "You can only input numbers" + COLOUR.END)
                else:
                    start_position: int = int(start_position)
                    end_position: int = int(end_position)

                    try:
                        self.move(start_position, end_position)
                    except Exception as e:
                        print(COLOUR.RED + str(e) + COLOUR.END + "\n\n")
            else:
                self.calculate_next_move()

        winner = self.game.get_winner()
        print(COLOUR.GREEN + f"The winner is player {winner}." + COLOUR.END)

    def move(self, start_position: int, end_position: int):
        """
        Move a piece
        :param start_position: The starting coordinates of the piece
        :param end_position: The end coordinates of the piece
        """

        self.game.move([start_position, end_position])

    @staticmethod
    def get_active_pieces(game: Game) -> List[Piece]:
        """
        Get the active pieces of a game
        :param game: The Game
        :return: A list of still available pieces
        """

        piece_list: list = []
        for piece in game.board.pieces:
            if not piece.captured:
                piece_list.append(piece)

        return piece_list

    @abstractmethod
    def calculate_next_move(self) -> Optional[dict]:
        """
        Has to be overwritten
        :return: The dict with the move and the score of the move
        """

    def get_move_by_pieces(self, transmitted_piece_list: List[CheckersPiece]) -> List[Tuple[int, int]]:
        """
        Get all the pieces on a board and reconstruct the moves which have been made.
        :param transmitted_piece_list: A list of pieces

        :raises: ValueError: If two pieces are at the same position
        :raises ValueError: If more than one piece moved for the current player
        :raises ValueError: If no piece moved for the current player
        :raises ValueError: The move was not possible

        :return: The moves which have been made
        """

        # Get a list of active pieces
        active_pieces: List[Piece] = self.get_active_pieces(self.game)

        # Generate a Hash map of pieces with the position as key
        piece_hash_map: Dict[int, CheckersPiece] = self.position_piece_hash_map(transmitted_piece_list)

        # A list of positions which have changed
        changed_positions: List[int] = self.get_changed_positions(active_pieces, piece_hash_map)

        # Try to reconstruct the game and return the move which made it possible
        moves: List[Tuple[int, int]] = self.reconstruct_game(changed_positions, piece_hash_map)
        return moves

    def get_changed_positions(self, active_pieces: List[Piece], piece_hash_map: Dict[int, CheckersPiece]) -> List[int]:
        """
        Get the positions where something has changed
        :param active_pieces: The currently active pieces in the game
        :param piece_hash_map: The new game's pieces as position piece hash map

        :return: The positions which changed for the current player
        """

        changed_positions: List[int] = []
        for piece in active_pieces:
            if not self.has_equivalent(piece, piece_hash_map, self.game.whose_turn()):
                changed_positions.append(piece.position)
        return changed_positions

    @staticmethod
    def has_equivalent(piece: Piece, piece_dict: Dict[int, CheckersPiece], player: Optional[int] = None) -> bool:
        """
        Check if a transmitted piece has a equivalent in the piece list
        :param piece: A piece which should have an equivalent
        :param piece_dict: A dict with position - piece
        :param player: Optional check if the piece belongs to a specific player

        :return: A bool value if the piece has an equivalent
        """

        if piece.position in piece_dict:
            if piece.player == piece_dict[piece.position].player:
                if piece.king == piece_dict[piece.position].king:
                    if piece.player != player or not player:
                        return True
        return False

    @staticmethod
    def position_piece_hash_map(pieces_list: List[CheckersPiece]) -> Dict[int, CheckersPiece]:
        """
        Build a hash map out of the pieces
        :param pieces_list: The pieces the hash map will be generated with

        :raises: ValueError: If two pieces are at the same position

        :return: The generated hash map
        """

        return_dict = {}
        for piece in pieces_list:
            if piece.position in return_dict:
                raise ValueError('There are two pieces at the same position')

            return_dict[piece.position] = piece

        return return_dict

    def reconstruct_game(self, changed_position: List[int], piece_hash_map: Dict[int, CheckersPiece]) \
            -> List[Tuple[int, int]]:
        """
        Try to reconstruct the game by taking a look at the changed positions
        :param piece_hash_map: The new game's pieces as position piece hash map
        :param changed_position: A list with one entry with the changed position for the current player

        :raises ValueError: If more than one piece moved for the current player
        :raises ValueError: If no piece moved for the current player
        :raises ValueError: The move was not possible

        :return: The moves which where made
        """

        player: int = self.game.whose_turn()

        if len(changed_position) > 1:
            raise ValueError(
                'More than one position has changed for the player which has to make a move. This is not possible')

        if len(changed_position) == 0:
            raise ValueError('Non of the players pieces has moved. This is not possible')

        changed_position: int = changed_position[0]
        move_list: List[Tuple[int, int]] = self.game.get_possible_moves()

        updated_move_list: List[Tuple[int, int]] = []
        for move in move_list:
            if move[0] == changed_position:
                updated_move_list.append(move)

        # Get the move and the resulting game
        game_move_list: List[Tuple[List[Tuple[int, int]], Game]] = []
        for move in updated_move_list:
            game_move_list.append(*self.trace_move(self.game, move, player))

        for game_move in game_move_list:
            possible_move_list: List[Tuple[int, int]] = game_move[0]
            game: Game = game_move[1]

            # Get the active pieces of the game
            active_pieces = self.get_active_pieces(game)

            # Check if anything is different (which should not be the case if the right moves where made)
            if not self.get_changed_positions(active_pieces, piece_hash_map):
                return possible_move_list

        raise ValueError('The move you tried is not possible')

    @staticmethod
    def trace_move(game: Game, move, player: int) -> List[Tuple[List[Tuple[int, int]], Game]]:
        """
        Trace the moves to the end

        :param game: The current game state
        :param move: The move which should be made
        :param player: The player which should make the move
        :return: A list of possible moves with the finished game state
        """

        return_list: List[Tuple[List[Tuple[int, int]], Game]] = []

        game: Game = deepcopy(game)
        game.move(move)

        # Check if the move of the player has ended
        if game.whose_turn() != player:
            return_list.append(([move], game))
        else:
            # TODO multi hop moves with different outcomes
            pass
        return return_list
