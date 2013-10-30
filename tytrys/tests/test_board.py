from tytrys.objects import Board, Coordinate
from unittest import TestCase

#todo: test lock_coordinates()


class TestBoard(TestCase):
    def test_initialization(self):
        """Board should be initialized with specified size, rows should be empty"""
        board = Board(20, 40)
        self.assertEqual(board.width, 20)
        self.assertEqual(board.height, 40)

        rows = board.rows
        self.assertEqual(len(rows), 40)
        self.assertEqual(len(rows[0]), 20)

    def test_are_valid_coordinates_with_valid_coordinates(self):
        board = Board(20, 40)

        # (0,0) is the a valid coordinate, indicating bottom-left
        coordinates = [Coordinate(0, 0)]
        self.assertTrue(board.are_valid_coordinates(coordinates))

        # check other corners
        coordinates = [Coordinate(0, 0),
                       Coordinate(19, 0),
                       Coordinate(0, 39),
                       Coordinate(19, 39)]
        self.assertTrue(board.are_valid_coordinates(coordinates))

    def test_are_valid_coordinates_with_invalid_coordinates(self):
        def check_coordinates(*coordinates):
            board = Board(20, 40)
            self.assertFalse(board.are_valid_coordinates(coordinates))

        check_coordinates(Coordinate(-1, 0),
                          Coordinate(1, 19),
                          Coordinate(0, 39),
                          Coordinate(19, 39))
        check_coordinates(Coordinate(0, 0),
                          Coordinate(1, 40),
                          Coordinate(0, 39),
                          Coordinate(19, 39))
        check_coordinates(Coordinate(0, 0),
                          Coordinate(1, 19),
                          Coordinate(0, 39),
                          Coordinate(19, 40))
        check_coordinates(Coordinate(0, 0),
                          Coordinate(1, 19),
                          Coordinate(0, 39),
                          Coordinate(20, 20))
        check_coordinates(Coordinate(0, 0),
                          Coordinate(15, -1),
                          Coordinate(0, 39),
                          Coordinate(19, 39))

    def test_clear_full_rows_with_no_full_rows(self):
        board = Board(20, 40)
        count = board.clear_full_rows()
        self.assertEqual(count, 0)

    def test_clear_full_rows_with_one_full_row(self):
        board = Board(20, 40)
        board.rows[0] = [1]*20
        count = board.clear_full_rows()
        self.assertEqual(count, 1)
        count = board.clear_full_rows()
        self.assertEqual(count, 0)

    def test_clear_full_rows_with_three_full_rows(self):
        board = Board(20, 40)
        board.rows[0] = [1] * 20
        board.rows[10] = [1] * 20
        board.rows[35] = [1] * 20
        board.rows[30] = [1, None] * 10
        count = board.clear_full_rows()
        self.assertEqual(count, 3)
