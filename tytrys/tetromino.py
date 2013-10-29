from tytrys.basic import Coordinate


class Base(object):
    """
    Defines methods used by all tetrominoes
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.coords = self.__class__.generate_coordinate(x, y)

    @classmethod
    def generate_coordinate(cls, x, y):
        return []


class Square(Base):
    @classmethod
    def generate_coordinate(cls, x, y):
        return [Coordinate(x, y),
                Coordinate(x+1, y),
                Coordinate(x+1, y-1),
                Coordinate(x, y-1)]