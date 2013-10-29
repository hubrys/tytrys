from tytrys.basic import Coordinate
from unittest import TestCase


class TestCoord(TestCase):

    def test_default_initialization(self):
        """
        default initialization should return a Coordinate representing (0,0)
        """
        coord = Coordinate.zero()
        self.assertEqual(coord.x, 0)
        self.assertEqual(coord.y, 0)

    def test_custom_initialization(self):
        """
        Custom initialization(X,Y) should return a Coordinate representing (X,Y)
        """
        coord = Coordinate(5, -9)
        self.assertEqual(coord.x, 5)
        self.assertEqual(coord.y, -9)

    def test_get_new_down(self):
        """
        get_new_down should return a new Coordinate with y coordinate 1 less than original
        """
        coord = Coordinate(10, 20).get_new_down()
        self.assertEqual(coord.x, 10)
        self.assertEqual(coord.y, 19)

    def test_get_new_up(self):
        """
        get_new_up should return a new Coordinate with y coordinate 1 more than original
        """
        coord = Coordinate(10, 20).get_new_up()
        self.assertEqual(coord.x, 10)
        self.assertEqual(coord.y, 21)

    def test_get_new_left(self):
        """
        get_new_left should return a new Coordinate with x coordinate 1 less than original
        """
        coord = Coordinate(10, 20).get_new_left()
        self.assertEqual(coord.x, 9)
        self.assertEqual(coord.y, 20)

    def test_get_new_right(self):
        """
        get_new_right should return a new Coordinate with x coordinate 1 more than original
        """
        coord = Coordinate(10, 20).get_new_right()
        self.assertEqual(coord.x, 11)
        self.assertEqual(coord.y, 20)