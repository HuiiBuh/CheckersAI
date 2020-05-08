import multiprocessing
from multiprocessing import Queue
from multiprocessing.context import Process
from multiprocessing.process import BaseProcess
from typing import List, Tuple, Optional

from checkers.game import Game
from sys import maxsize

from .MinMax import MinMax


class MinMaxWeight:
    WIN = maxsize
    LOSE = -maxsize
    POSITION = 1
    PIECE = 66
    KING = 10


class MinMaxMP(MinMax):

    def _start_min_max(self) -> List[Tuple[float, Optional[int]]]:

        cpu_cores: int = multiprocessing.cpu_count()

        move_list = self.game.get_possible_moves()
        process_move_list = [move_list[i::cpu_cores] for i in range(len(move_list))]

        communication_queue = Queue()

        # Create the processes
        process_list: List[BaseProcess] = []
        for process_number in range(len(process_move_list)):
            # Args for the process
            args: tuple = (self.game, process_move_list[process_number], communication_queue)

            # Create the new process
            process: BaseProcess = Process(target=self._min_max, args=args, name=f"Checkers Process: {process_number}")

            # Start the process
            process.start()
            process_list.append(process)

        # Wait for the processes to terminate
        for process in process_list:
            process.join()

        # Get the results from the queue
        result_list = []
        while not communication_queue.empty():
            result_list.append(communication_queue.get())

        # Close the queue
        communication_queue.close()
        communication_queue.join_thread()

        return result_list


    def _min_max(self, game: Game, move_list: List[Tuple[int, int]], queue: Queue = None, **kwargs) -> None:
        """
        Calculate the min max
        :param game: The game
        :param move_list: A list of moves
        :param queue: The communication queue
        """

        best_score, best_move = MinMax._min_max(self, game, True, move_list)

        queue.put([best_score, best_move])
