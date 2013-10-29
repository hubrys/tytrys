from functools import total_ordering

@total_ordering
class Coordinate(object):
    """holds x,y coordinates to a point (integer)"""

    def __init__(self, x, y):
        """Set x and y values of new Coordinate to values"""
        self.x = x
        self.y = y

    def 
    @classmethod
    def zero(cls):
        """Return a Coordinate object initialized to (0,0)."""
        return cls(0, 0)

    def get_new_down(self):
        """Return a Coordinate object one lower than caller."""
        return Coordinate(self.x, self.y - 1)

    def get_new_up(self):
        """Return a Coordinate object one hgiher than caller."""
        return Coordinate(self.x, self.y + 1)

    def get_new_left(self):
        """Return a Coordinate object one to the left of caller."""
        return Coordinate(self.x - 1, self.y)

    def get_new_right(self):
        """Return a Coordinate object one to the right of caller."""
        return Coordinate(self.x + 1, self.y)


class Direction(object):
    Up = 0
    Down = 1
    Left = 2
    Right = 3
    CW = 4
    CCW = 5