import curses
from states import GameState, Status
import renderer
from renderer import Color
from objects import Board, Square


def main(main_window):
    #board = Board(30, 40)
    #board_window = main_window.subwin(board.height+2, board.width+2, 2, 2)
    #square = Square(28, 40)
    #renderer.draw_board(board, board_window)
    #renderer.draw_tetromino(square, main_window)
    #renderer.draw_tetromino(square, board_window)
    #board_window.refresh()
    #main_window.getch()
    renderer.initialize()
    game_state = GameState(main_window)
    while game_state.status != Status.Finished:
        game_state.update(1)


curses.wrapper(main)