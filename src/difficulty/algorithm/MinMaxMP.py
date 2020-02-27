import copy
import multiprocessing
import random
from multiprocessing import Queue
from multiprocessing.context import Process
from multiprocessing.process import BaseProcess
from sys import maxsize
from typing import List, Optional

from checkers.game import Game

from . import MinMax


class MinMaxWeight:
    WIN = maxsize
    LOSE = -maxsize
    POSITION = 1
    PIECE = 6
    KING = 10


class MinMaxMP(MinMax):

    def _start_min_max(self) -> list:

        cpu_cores: int = multiprocessing.cpu_count()

        move_list = self.game.get_possible_moves()
        process_move_list = [move_list[i::cpu_cores] for i in range(len(move_list))]

        communication_queue = Queue()

        # Create the processes
        process_list: List[BaseProcess] = []
        for process_number in range(len(process_move_list)):
            # Args for the process
            kwargs: dict = {'move_list': move_list, 'queue': communication_queue}
            args: tuple = (self.game, True)

            # Create the new process
            process: BaseProcess = Process(target=self._min_max, name=f"Checkers Process: {process_number}",
                                           args=args, kwargs=kwargs)
            # Start the process
            process.start()
            process_list.append(process)

        # Wait for the processes to terminate
        for process_number in range(len(process_list)):
            process_list[process_number].join()

        # Get the results from the queue
        result_list = []
        while not communication_queue.empty():
            result_list.append(communication_queue.get())

        # Create the list with the best moves
        result_best_move = [MinMaxWeight.LOSE, []]  # type: List[int, List[int]]

        # Go through every move in the list
        for result in result_list:

            # Get the score and check if the score is better than the score of the current best move
            score = result[0]
            if score > result_best_move[0]:
                result_best_move[0] = score
                result_best_move[1] = result[1]

        # Close the queue
        communication_queue.close()
        communication_queue.join_thread()

        return result_best_move

    def _min_max(self,
                 game: Game,
                 maximize_score: bool,
                 move_list: list = None,
                 queue: Queue = None,
                 alpha=MinMaxWeight.LOSE,
                 beta=MinMaxWeight.WIN,
                 depth=0) -> List[Optional[int]]:
        """
        Calculate the min max
        :param depth: The current depth of the branch
        :return:
        """

        # Check if the game is over
        if game.is_over():
            winner = game.get_winner()
            if winner == self.player:
                return [MinMaxWeight.WIN, None]
            return [MinMaxWeight.LOSE, None]

        # Check if the max depth is reached
        if depth >= self.branch_depth:
            return [self.evaluate_path(game), None]

        # Get the smallest/largest number to initialize the var
        best_score: float = MinMaxWeight.LOSE if maximize_score else MinMaxWeight.WIN
        best_move = None

        if not move_list:
            move_list = game.get_possible_moves()
            move_list = random.sample(move_list, len(move_list))

        # Iterate through the moves and recursively find the best
        for move in move_list:
            updated_game = copy.deepcopy(game)
            updated_game.move(move)
            returned_best_score, _ = self._min_max(updated_game, not maximize_score,
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

        if queue:
            queue.put([best_score, best_move])

        return [best_score, best_move]
