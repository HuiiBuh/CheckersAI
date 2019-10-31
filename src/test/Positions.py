import unittest

from difficulty.Opponent import Opponent


class TestPosition(unittest.TestCase):
    def setUp(self):
        self.opponent = Opponent(1)

    def test_position_to_coordinates(self):
        coordinates = self.opponent._position_to_coordinates(9)
        self.assertEqual(("B", "6"), coordinates)

    def test_coordinates_to_position(self):
        position = self.opponent._coordinates_to_position(["C", 3])
        self.assertEqual(22, position)


if __name__ == '__main__':
    unittest.main()
