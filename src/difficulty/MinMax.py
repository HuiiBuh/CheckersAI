import copy
import random
import time
import multiprocessing
from multiprocessing import Process, Array
from sys import maxsize
from pip._vendor.msgpack.fallback import xrange

from checkers.game import Game

from difficulty.Opponent import Opponent


class MinMaxWeight:
    WIN = maxsize
    LOSE = -maxsize
    POSITION = 1
    PIECE = 6
    KING = 10


class MinMax(Opponent):
    def __init__(self, player: int, branch_depth: int):
        """
        Create a new MinMax Opponent
        :param player: The player number
        :param branch_depth: The depth of the min max calculation
        """
        super().__init__(player)
        self.branch_depth: int = branch_depth

    def make_next_move(self):
        """
        Make a move based on the min max algorithm
        :return: None
        """

        # Check if it is the turn of the computer
        if self.game.whose_turn() is not self.player:
            return

        start = time.time()
        score, move = self._start_min_max()
        
        print(time.time() - start)
        print("")
        print(f"Score: {score}")
        print(f"Move: {self._position_to_coordinates(move[0])}/{self._position_to_coordinates(move[1])}")

        self.game.move(move)

    def _start_min_max(self):
        # Get the CPU count
        cores = multiprocessing.cpu_count()

        # Get the possible moves and split them for each cpu
        possible_moves = self.game.get_possible_moves()
        possible_moves = random.sample(possible_moves, len(possible_moves))
        possible_moves = [possible_moves[i::cores] for i in xrange(cores)]

        # List with the processes
        process_list = []

        # The shared variables
        process_move_list = Array("i", range(cores * 3))

        # Create a process for each coer
        for i in range(cores):
            moves = possible_moves[i]
            position = i * 3

            process_list.append(
                Process(target=self._min_max, args=(self.game, True),
                        kwargs={"possible_moves": moves, "thread_move_list": process_move_list, "position": position}))
            process_list[i].start()

        # Join all cores
        for i in range(cores):
            process_list[i].join()

        best_score_move = [MinMaxWeight.LOSE, []]

        # Get the best score
        for i in range(0, len(process_move_list) - 1, 3):
            score = process_move_list[i]
            if score > best_score_move[0]:
                move_1 = process_move_list[i + 1]
                move_2 = process_move_list[i + 2]
                best_score_move = [score, [move_1, move_2]]

            i += 2

        # Return the best move
        return best_score_move

    def _min_max(self, game: Game, maximize_score: bool, alpha=MinMaxWeight.LOSE, beta=MinMaxWeight.WIN, depth=0,
                 possible_moves=None, thread_move_list=None, position=None):
        """
        Calculate the min max
        :param depth: The current depth of the branch
        :return:
        """

        # Check if the game is over
        if thread_move_list is None:
            thread_move_list = []
        if game.is_over():
            winner = game.get_winner()
            if winner == self.player:
                return MinMaxWeight.WIN, None
            return MinMaxWeight.LOSE, None

        # Check if the max depth is reached
        if depth >= self.branch_depth:
            return self.evaluate_path(game), None

        # Get the smallest/largest number to initialize the var
        best_score: float = MinMaxWeight.LOSE if maximize_score else MinMaxWeight.WIN
        best_move = None

        if not possible_moves:
            possible_moves = game.get_possible_moves()
            possible_moves = random.sample(possible_moves, len(possible_moves))

        # Iterate through the moves and recursively find the best
        for move in possible_moves:
            updated_game = copy.deepcopy(game)
            updated_game.move(move)
            returned_best_score, returned_best_move = self._min_max(updated_game, not maximize_score,
                                                                    alpha=alpha,
                                                                    beta=beta,
                                                                    depth=depth + 1)
            if maximize_score and best_score < returned_best_score:
                best_score = returned_best_score
                best_move = move
                alpha = max(alpha, best_score)

                if beta <= alpha:
                    break

            elif not maximize_score and returned_best_score < best_score:
                best_score = returned_best_score
                best_move = move
                beta = min(beta, best_score)

                if beta <= alpha:
                    break

        # Update the shared variables
        if thread_move_list:
            thread_move_list[position] = best_score
            thread_move_list[position + 1] = best_move[0]
            thread_move_list[position + 2] = best_move[1]

        return best_score, best_move

    def evaluate_path(self, game: Game):
        """
        Evaluates the score of the computer and the human at a certain point of the game
        :param game: The game that is supposed to be evaluated
        :return: The score (positive if the computer is better and visa versa)
        """

        computer_score = 0
        human_score = 0

        # For every piece in the ame
        for piece in self.get_active_pieces(self.game):

            # Get the owner of the piece
            if piece.player is self.player:
                # Get the type of the piece and add a value
                if piece.king:
                    computer_score += MinMaxWeight.KING
                else:
                    if self.player == 2 and int(piece.position / 4) <= 4:
                        computer_score += MinMaxWeight.POSITION
                    elif self.player == 1 and int(piece.position / 4) >= 5:
                        computer_score += MinMaxWeight.POSITION

                    computer_score += MinMaxWeight.PIECE
            else:
                # Get the type of the piece and add a value
                if piece.king:
                    human_score += MinMaxWeight.KING
                else:
                    if self.player == (3 - self.player) and int(piece.position / 4) >= 5:
                        human_score += MinMaxWeight.POSITION
                    elif self.player == (3 - self.player) and int(piece.position / 4) <= 4:
                        human_score += MinMaxWeight.POSITION

                    human_score += MinMaxWeight.PIECE

        return computer_score - human_score

    @staticmethod
    def get_active_pieces(game: Game) -> list:
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
