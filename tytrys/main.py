import curses
from states import PauseState, GameState, Status
import renderer
import time
import game

def main(window):
    renderer.initialize()

    curses.curs_set(0)
    dimens = window.getmaxyx()
    main_window = window.subwin(22, 20, dimens[0] // 2 - 11, dimens[1] // 2 - 10)
    main_window.nodelay(1)
    main_window.keypad(1)

    game.init()
    game.add_state("paused", PauseState(main_window))
    game.add_state_and_switch("game", GameState(main_window))
    game.run()


curses.wrapper(main)