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


def draw_board_square(window, x, y, color):
    dimensions = window.getmaxyx()
    # minus 1 is for window border
    window.addch(dimensions[0] - y - 1, x + 1, ord(' '), curses.color_pair(color))


def draw_board(board, window):
    window.border()


def draw_tetromino(tetromino, window):
    """Draw coordinates on screen for tetromino"""
    for coordinate in tetromino.coordinates:
        draw_board_square(window, coordinate.x, coordinate.y, tetromino.color)


def clear_tetromino(tetromino, window):
    """Clear coordinates on screen for tetromino"""
    for coordinate in tetromino.coordinates:
        draw_board_square(window, coordinate.x, coordinate.y, Color.Black)