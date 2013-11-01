import curses


class Color:
    Black = 0
    Red = 1
    Green = 2
    Yellow = 3
    Blue = 4
    Magenta = 5
    Cyan = 6
    White = 7


def initialize():
    initialize_colors()


def initialize_colors():
    curses.init_pair(Color.Red,     curses.COLOR_BLACK, curses.COLOR_RED)
    curses.init_pair(Color.Green,   curses.COLOR_BLACK, curses.COLOR_GREEN)
    curses.init_pair(Color.Yellow,  curses.COLOR_BLACK, curses.COLOR_YELLOW)
    curses.init_pair(Color.Blue,    curses.COLOR_BLACK, curses.COLOR_BLUE)
    curses.init_pair(Color.Magenta, curses.COLOR_BLACK, curses.COLOR_MAGENTA)
    curses.init_pair(Color.Cyan,    curses.COLOR_BLACK, curses.COLOR_CYAN)
    curses.init_pair(Color.White,   curses.COLOR_BLACK, curses.COLOR_WHITE)


def draw_square(x, y, color, window):
    dimensions = window.getmaxyx()
    if x < dimensions[1]-1 and y < dimensions[0]-2:
        window.addch(dimensions[0] - 2 - y, x + 1, ord(' '), curses.color_pair(color))


def draw_board(board, window):
    window.border()
    for y, row in enumerate(board.rows):
        for x, color in enumerate(row):
            draw_square(x, y, color if color is not None else Color.Black, window)


def draw_tetromino(tetromino, window):
    """Draw coordinates on screen for tetromino"""
    for coordinate in tetromino.coordinates:
        draw_square(coordinate.x, coordinate.y, tetromino.color, window)


def clear_tetromino(tetromino, window):
    """clears tetromino from screen"""
    for coordinate in tetromino.coordinates:
        draw_square(coordinate.x, coordinate.y, Color.Black, window)
