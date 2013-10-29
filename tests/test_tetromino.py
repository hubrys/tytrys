from tytrys.tetromino import Square
from tytrys.basic import Coord
from unittest import TestCase

class TestTetromino(TestCase):
    """
    The Tetromino tests are done with the Square since Base returns None for many
    of the functions. The square is the simplest piece and should work like Base +
    actual coordinates.

    """
    def test_initialization(self):
        square = Square(0, 0)
        self.assertEqual(square.x, 0)
        self.assertEqual(square.y, 0)

        coords = square.coords
        self.assertIsNotNone(coords)
        self.assertEqual(len(coords), 4)
        self.assertEqual(coords, [Coord(0, 0), Coord(1, 0), Coord(1, 1), Coord(0, 1)])

