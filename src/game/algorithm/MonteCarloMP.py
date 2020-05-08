import multiprocessing
import random
from multiprocessing import Queue
from multiprocessing.context import Process
from multiprocessing.process import BaseProcess
from typing import List, Optional, Dict, Any

from sys import maxsize

from game.algorithm.MonteCarlo import MonteCarlo


class MonteCarloMP(MonteCarlo):

    def _start_monte_carlo(self) -> Optional[List[Dict[str, Any]]]:

        # Check if it is the turn of the computer
        if self._game.whose_turn() is not self.player or self._game.is_over():
            return

        # Get the cpu cores
        cpu_cores: int = multiprocessing.cpu_count()

        # Get the possible moves
        move_list: list = self._game.board.get_possible_moves()
        random.shuffle(move_list)

        # Create a list with spited moves
        process_move_list = [move_list[i::cpu_cores] for i in range(len(move_list))]

        communication_queue = Queue()
        # Create the processes
        process_list: List[BaseProcess] = []
        for process_number in range(len(process_move_list)):
            # Args for the process
            args: tuple = (process_move_list[process_number], self._game, self.move_count, communication_queue)

            # Create the new process
            process: BaseProcess = Process(target=self._tree_search, args=args,
                                           name=f"Checkers Process: {process_number}")
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

    def _tree_search(self, move_list, game, move_count, queue: Queue = None):

        result_list = []
        for move in move_list:
            result = MonteCarlo._tree_search(self, move, game, move_count)
            result_list.append(result)

        best_move_score = {"move": None, "score": -maxsize}
        for move_score in result_list:
            if move_score["score"] > best_move_score["score"]:
                best_move_score = move_score

        queue.put(best_move_score)
