import unittest
from math import ceil

from difficulty.Opponent import Opponent


class TestPosition(unittest.TestCase):
    def setUp(self):
        self.opponent = Opponent(1)

    def test_position_to_coordinates(self):
        for position in range(1, 19):
            coordinates: tuple = self.opponent._position_to_coordinates(position)

            y: int = 9 - ceil(position / 4)

            if (position % 4) != 0:
                x: str = str(chr(2 * (position % 4) + (y % 2) + 64))
            else:
                x: str = str(chr(8 - (y % 2) + 64))
                y -= 1

            self.assertEqual((x, str(y)), coordinates)

    def test_coordinates_to_position(self):
        position = self.opponent._coordinates_to_position(["C", 3])
        self.assertEqual(22, position)

    if __name__ == '__main__':
        unittest.main()
