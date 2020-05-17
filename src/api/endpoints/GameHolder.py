import random
import string
from typing import Dict, Optional

from game.algorithm.Opponent import Opponent


class GameHolder:

    def __init__(self):
        self.game_instances: Dict[str, Opponent] = {}

    @staticmethod
    def random_string(length) -> str:
        """
        Get a random string
        :param length: The length of the string
        :return: The random string
        """

        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for _ in range(length))

    def add_game(self, game: Opponent) -> str:
        """
        Add a game to the Game holder class
        :param game: The game which should be saved
        :return: Return the game key
        """
        # Get a game key
        game_key = self.random_string(64)

        # Update the game key and update the key
        while game_key in self.game_instances:
            game_key = self.random_string(64)

        self.game_instances[game_key] = game
        return game_key

    def __getitem__(self, key: str) -> Optional[Opponent]:
        if key not in self.game_instances:
            return None

        return self.game_instances[key]

    def __contains__(self, key: str):
        return key in self.game_instances

    def __delitem__(self, key):
        del self.game_instances[key]
