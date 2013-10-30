from tytrys.objects import Coordinate, Square, Direction
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

        coords = square.coordinates
        self.assertIsNotNone(coords)
        self.assertEqual(len(coords), 4)
        self.assertEqual(coords,
                         [Coordinate(0, 0),
                          Coordinate(1, 0),
                          Coordinate(1, -1),
                          Coordinate(0, -1)])

    def test_move_result_down(self):
        """
        Move result should give coordinate like move but actual coords should not change
        """
        square = Square(0, 0)
        coords = square.coordinates
        results = square.move_result(Direction.Down)
        self.assertEqual(results,
                         [Coordinate(0, -1),
                          Coordinate(1, -1),
                          Coordinate(1, -2),
                          Coordinate(0, -2)])
        self.assertEqual(coords,
                         [Coordinate(0, 0),
                          Coordinate(1, 0),
                          Coordinate(1, -1),
                          Coordinate(0, -1)])

    def test_move_result_up(self):
        square = Square(0, 0)
        coords = square.coordinates
        results = square.move_result(Direction.Up)
        self.assertEqual(results,
                         [Coordinate(0, 1),
                          Coordinate(1, 1),
                          Coordinate(1, 0),
                          Coordinate(0, 0)])
        self.assertEqual(coords,
                         [Coordinate(0, 0),
                          Coordinate(1, 0),
                          Coordinate(1, -1),
                          Coordinate(0, -1)])

    def test_move_result_left(self):
        square = Square(0, 0)
        coords = square.coordinates
        results = square.move_result(Direction.Left)
        self.assertEqual(results,
                         [Coordinate(-1, 0),
                          Coordinate(0, 0),
                          Coordinate(0, -1),
                          Coordinate(-1, -1)])
        self.assertEqual(coords,
                         [Coordinate(0, 0),
                          Coordinate(1, 0),
                          Coordinate(1, -1),
                          Coordinate(0, -1)])

    def test_move_result_right(self):
        square = Square(0, 0)
        coords = square.coordinates
        results = square.move_result(Direction.Right)
        self.assertEqual(results,
                         [Coordinate(1, 0),
                          Coordinate(2, 0),
                          Coordinate(2, -1),
                          Coordinate(1, -1)])
        self.assertEqual(coords,
                         [Coordinate(0, 0),
                          Coordinate(1, 0),
                          Coordinate(1, -1),
                          Coordinate(0, -1)])

    def test_move_down(self):
        square = Square(0, 0)
        square.move(Direction.Down)
        coords = square.coordinates
        self.assertIsNotNone(coords)
        self.assertEqual(len(coords), 4)
        self.assertEqual(coords,
                         [Coordinate(0, -1),
                          Coordinate(1, -1),
                          Coordinate(1, -2),
                          Coordinate(0, -2)])

    def test_move_up(self):
        square = Square(0, 0)
        square.move(Direction.Up)
        coords = square.coordinates
        self.assertIsNotNone(coords)
        self.assertEqual(len(coords), 4)
        self.assertEqual(coords,
                         [Coordinate(0, 1),
                          Coordinate(1, 1),
                          Coordinate(1, 0),
                          Coordinate(0, 0)])

    def test_move_left(self):
        square = Square(0, 0)
        square.move(Direction.Left)
        coords = square.coordinates
        self.assertIsNotNone(coords)
        self.assertEqual(len(coords), 4)
        self.assertEqual(coords,
                         [Coordinate(-1, 0),
                          Coordinate(0, 0),
                          Coordinate(0, -1),
                          Coordinate(-1, -1)])

    def test_move_right(self):
        square = Square(0, 0)
        square.move(Direction.Right)
        coords = square.coordinates
        self.assertIsNotNone(coords)
        self.assertEqual(len(coords), 4)
        self.assertEqual(coords,
                         [Coordinate(1, 0),
                          Coordinate(2, 0),
                          Coordinate(2, -1),
                          Coordinate(1, -1)])