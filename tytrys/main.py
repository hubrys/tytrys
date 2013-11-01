import curses
from states import PauseState, GameState, Status
import renderer
import time


def main(window):
    curses.curs_set(0)
    dimens = window.getmaxyx()
    main_window = window.subwin(22, 20, dimens[0] // 2 - 11, dimens[1] // 2 - 10)
    main_window.nodelay(1)
    main_window.keypad(1)
    renderer.initialize()
    game_state = GameState(main_window)
    last = time.clock()
    while game_state.status != Status.Finished:
        now = time.clock()
        game_state.update(now - last)
        if game_state.status == Status.Paused:
            pause_state = PauseState(main_window)
            pause_state.update(0)
            game_state.status = pause_state.status
            game_state.view_modified = True
            now = time.clock()
            if game_state.status == Status.Restart:
                game_state.restart()
        last = now


curses.wrapper(main)