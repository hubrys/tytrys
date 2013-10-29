class Coord(object):
    """holds x,y coordinates to a point (integer)"""

    def __init__(self, x, y):
        """Set x and y values of new Coord to values"""
        self.x = x
        self.y = y

    @classmethod
    def zero(cls):
        """Return a Coord object initialized to (0,0)."""
        return cls(0, 0)

    def get_new_down(self):
        """Return a Coord object one lower than caller."""
        return Coord(self.x, self.y - 1)

    def get_new_up(self):
        """Return a Coord object one hgiher than caller."""
        return Coord(self.x, self.y + 1)

    def get_new_left(self):
        """Return a Coord object one to the left of caller."""
        return Coord(self.x - 1, self.y)

    def get_new_right(self):
        """Return a Coord object one to the right of caller."""
        return Coord(self.x + 1, self.y)

