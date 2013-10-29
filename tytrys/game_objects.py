from functools import total_ordering


class Direction(object):
    Up = 0
    Down = 1
    Left = 2
    Right = 3
    CW = 4
    CCW = 5


@total_ordering
class Coordinate(object):
    """holds x,y coordinates to a point (integer)"""
    def __init__(self, x, y):
        """Set x and y values of new Coordinate to values"""
        self.x = x
        self.y = y

    @classmethod
    def zero(cls):
        """Return a Coordinate object initialized to (0,0)."""
        return cls(0, 0)

    def __eq__(self, other):
        return (self.x == other.x) and (self.y == other.y)

    def __lt__(self, other):
        return (self.x < other.x) and (self.y < other.y)

    def get_new(self, direction):
        """Return a Coordinate one unit in direction specified"""
        if direction == Direction.Up:
            return Coordinate(self.x, self.y + 1)
        elif direction == Direction.Down:
            return Coordinate(self.x, self.y - 1)
        elif direction == Direction.Left:
            return Coordinate(self.x - 1, self.y)
        elif direction == Direction.Right:
            return Coordinate(self.x + 1, self.y)
        return None


class Board(object):
    """Defines playable area, holds locked pieces"""
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.rows = [[None]*width for x in range(height)]

    def are_valid_coordinates(self, coordinates):
        """
        Return true if all coordinates are valid on this Board

        coordinate is valid if between points (0,0) and (width, height)"""
        for coordinate in coordinates:
            if not ((0 <= coordinate.x < self.width)
                    and (0 <= coordinate.y < self.height)
                    and (self.rows[coordinate.y][coordinate.x] is None)):
                return False
        return True

    def lock_coordinates(self, coordinates, lock_value):
        """
        Lock passed coordinates to board with lock_value,
        throws RuntimeException if coordinates are not valid

        """
        if not self.are_valid_coordinates(coordinates):
            raise RuntimeError('Tired to lock invalid coordinates')

        for coordinate in coordinates:
            self.rows[coordinate.y][coordinates.x] = lock_value

    def clear_full_rows(self):
        """Remove filled rows and Return number of removed rows"""
        old_count = len(self.rows)
        self.rows = [row for row in self.rows if None in row]
        rows_removed = old_count - len(self.rows)
        for x in range(rows_removed):
            self.rows.append([None]*self.width)
        return rows_removed


class Tetromino(object):
    """
    Defines methods used by all tetrominoes
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.coordinates = self.__class__.generate_coordinate(x, y)

    @classmethod
    def generate_coordinate(cls, x, y):
        """
        generates coordinates for shape at (x,y),
        default implementation returns empty list
        """
        return []

    def move(self, direction):
        """Move Tetromino one unit in specified direction"""
        self.coordinates = self.move_result(direction)

    def move_result(self, direction):
        """Return coordinates of Tetromino if move(direction) was called"""
        return [x.get_new(direction) for x in self.coordinates]


class Square(Tetromino):
    """defines behavior for square tetromino"""
    @classmethod
    def generate_coordinate(cls, x, y):
        return [Coordinate(x, y),
                Coordinate(x+1, y),
                Coordinate(x+1, y-1),
                Coordinate(x, y-1)]