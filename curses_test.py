import curses


def main(screen):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_WHITE)
    screen.addch(5, 5, ord('A'), curses.color_pair(1))
    screen.refresh()
    screen.getch()


curses.wrapper(main)
