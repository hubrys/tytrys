import random
from functools import total_ordering
from renderer import Color


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
        self.rows = [[None] * width for x in range(height)]

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

    def lock_tetromino(self, tetromino):
        """
        Lock passed coordinates to board with lock_value,
        throws RuntimeException if coordinates are not valid

        """
        if not self.are_valid_coordinates(tetromino.coordinates):
            raise RuntimeError('Tried to lock invalid coordinates')

        for coordinate in tetromino.coordinates:
            self.rows[coordinate.y][coordinate.x] = tetromino.color

    def clear_full_rows(self):
        """Remove filled rows and Return number of removed rows"""
        old_count = len(self.rows)
        self.rows = [row for row in self.rows if None in row]
        rows_removed = old_count - len(self.rows)
        for x in range(rows_removed):
            self.rows.append([None] * self.width)
        return rows_removed


class Tetromino(object):
    """
    Defines methods used by all tetrominoes
    """

    def __init__(self, x, y, color=Color.Green):
        self.x = x
        self.y = y
        self.color = color
        self.rotation = 0
        self.coordinates = self.__class__.generate_coordinates(x, y, self.rotation)

    @classmethod
    def generate_coordinates(cls, x, y, direction):
        """
        generates coordinates for shape at (x,y),
        default implementation returns empty list
        """
        return []

    def set_location(self, x, y):
        self.coordinates = self.__class__.generate_coordinates(x, y, self.rotation % 4)
        self.x, self.y = x, y

    def move(self, direction):
        """Move Tetromino one unit in specified direction"""
        self.coordinates = self.move_result(direction)
        self.x, self.y = self.coordinates[0].x, self.coordinates[0].y

    def move_result(self, direction):
        """Return coordinates of Tetromino if move(direction) was called"""
        return [x.get_new(direction) for x in self.coordinates]

    def rotate(self, direction):
        if direction == Direction.CCW:
            self.rotation += 1
        else:
            self.rotation -= 1
        self.coordinates = self.__class__.generate_coordinates(self.x, self.y, self.rotation % 4)

    def rotate_result(self, direction):
        if direction == Direction.CCW:
            rotation = self.rotation + 1
        else:
            rotation = self.rotation - 1
        return self.__class__.generate_coordinates(self.x, self.y, rotation % 4)


class Square(Tetromino):
    """defines behavior for square tetromino"""

    @classmethod
    def generate_coordinates(cls, x, y, direction):
        return [Coordinate(x, y),
                Coordinate(x + 1, y),
                Coordinate(x + 1, y - 1),
                Coordinate(x, y - 1)]


class Line(Tetromino):
    """defines behavior of line tetromino"""

    @classmethod
    def generate_coordinates(cls, x, y, direction):
        if direction % 2 == 0:
            return [Coordinate(x, y),
                    Coordinate(x - 1, y),
                    Coordinate(x + 1, y),
                    Coordinate(x + 2, y)]
        else:
            return [Coordinate(x, y),
                    Coordinate(x, y + 1),
                    Coordinate(x, y - 1),
                    Coordinate(x, y - 2)]


class Zig(Tetromino):
    """Defines behavior of zig tetromino"""

    @classmethod
    def generate_coordinates(cls, x, y, direction):
        if direction % 2 == 0:
            return [Coordinate(x, y),
                    Coordinate(x - 1, y),
                    Coordinate(x, y + 1),
                    Coordinate(x + 1, y + 1)]
        else:
            return [Coordinate(x, y),
                    Coordinate(x, y - 1),
                    Coordinate(x - 1, y),
                    Coordinate(x - 1, y + 1)]


class Zag(Tetromino):
    """Defines behavior of zig tetromino"""
    @classmethod
    def generate_coordinates(cls, x, y, direction):
        if direction % 2 == 0:
            return [Coordinate(x, y),
                    Coordinate(x + 1, y),
                    Coordinate(x, y + 1),
                    Coordinate(x - 1, y + 1)]
        else:
            return [Coordinate(x, y),
                    Coordinate(x, y - 1),
                    Coordinate(x + 1, y),
                    Coordinate(x + 1, y + 1)]


class Ell(Tetromino):
    """defines behavior of reverse-ell tetromino"""

    @classmethod
    def generate_coordinates(cls, x, y, orientation):
        if orientation == 3:
            return [Coordinate(x, y),
                    Coordinate(x - 1, y),
                    Coordinate(x + 1, y),
                    Coordinate(x + 1, y + 1)]
        if orientation == 0:
            return [Coordinate(x, y),
                    Coordinate(x, y + 1),
                    Coordinate(x, y - 1),
                    Coordinate(x + 1, y - 1)]

        if orientation == 1:
            return [Coordinate(x, y),
                    Coordinate(x - 1, y),
                    Coordinate(x - 1, y - 1),
                    Coordinate(x + 1, y)]
        else:
            return [Coordinate(x, y),
                    Coordinate(x, y + 1),
                    Coordinate(x - 1, y + 1),
                    Coordinate(x, y - 1)]


class ReverseEll(Tetromino):
    """defines behavor of ell tetromino"""

    @classmethod
    def generate_coordinates(cls, x, y, orientation):
        if orientation == 1:
            return [Coordinate(x, y),
                    Coordinate(x - 1, y),
                    Coordinate(x - 1, y + 1),
                    Coordinate(x + 1, y)]
        elif orientation == 2:
            return [Coordinate(x, y),
                    Coordinate(x, y - 1),
                    Coordinate(x, y + 1),
                    Coordinate(x + 1, y + 1)]
        elif orientation == 3:
            return [Coordinate(x, y),
                    Coordinate(x - 1, y),
                    Coordinate(x + 1, y),
                    Coordinate(x + 1, y - 1)]
        else:
            return [Coordinate(x, y),
                    Coordinate(x, y + 1),
                    Coordinate(x, y - 1),
                    Coordinate(x - 1, y - 1)]


class Tee(Tetromino):
    """defines behavior of Tee tetromino"""

    @classmethod
    def generate_coordinates(cls, x, y, orientation):
        if orientation == 0:
            return [Coordinate(x, y),
                    Coordinate(x - 1, y),
                    Coordinate(x + 1, y),
                    Coordinate(x, y + 1)]
        if orientation == 1:
            return [Coordinate(x, y),
                    Coordinate(x, y + 1),
                    Coordinate(x + 1, y),
                    Coordinate(x, y - 1)]
        if orientation == 2:
            return [Coordinate(x, y),
                    Coordinate(x - 1, y),
                    Coordinate(x + 1, y),
                    Coordinate(x, y - 1)]
        else:
            return [Coordinate(x, y),
                    Coordinate(x, y + 1),
                    Coordinate(x - 1, y),
                    Coordinate(x, y - 1)]


tetrominoes = ((Square, Color.Green),
               (Line, Color.Blue),
               (Zig, Color.Cyan),
               (Zag, Color.White),
               (Ell, Color.Magenta),
               (ReverseEll, Color.Red),
               (Tee, Color.Yellow))


def random_tetromino(x, y):
    tetromino = random.choice(tetrominoes)
    return tetromino[0](x, y, tetromino[1])