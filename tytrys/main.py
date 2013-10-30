import curses
import renderer
from renderer import Color
from objects import Board, Square

def main(main_window):
    board = Board(30, 40)
    board_window = main_window.subwin(board.height+2, board.width+2, 2, 2)
    square = Square(28, 40)
    square.color = Color.Red
    renderer.initialize()
    renderer.draw_board(None, board_window)
    renderer.draw_tetromino(square, main_window)
    renderer.draw_tetromino(square, board_window)
    board_window.refresh()
    main_window.getch()

curses.wrapper(main)