import curses
from states import GameState, Status
import renderer
from renderer import Color
from objects import Board, Square


def main(main_window):
    main_window.nodelay(1)
    renderer.initialize()
    game_state = GameState(main_window)
    while game_state.status != Status.Finished:
        game_state.update(1)


curses.wrapper(main)