from objects import Board, Direction, random_tetromino
import curses
import renderer
import game
from game import Status


class TytrysState(game.State):
    """Provides information common to all states in Tytrys"""

    def __init__(self, window):
        """Initializes TytrysState object

        Arguments:
        window -- curses.Window state should draw to

        """
        super().__init__()
        self.window = window
        self.elapsed_time = 0


class GameState(TytrysState):
    """Game Logic

    """

    def __init__(self, window):
        super(GameState, self).__init__(window)
        # These lines are so that I don't have to stare at warnings
        # restart sets these to the right values
        self.board = Board(10, 22)
        self.next_piece = random_tetromino(0, 0)
        self.current_piece = random_tetromino(5, 20)
        self.drop_time = .5
        self.current_key = -1
        self.lines_to_next_level = 15
        self.level = 1
        self.score = 0
        self.view_modified = True

        self._restart()
        self.board_window = window.derwin(
            self.board.height, self.board.width + 2, 0, 0)
        self.info_window = window.derwin(
            self.board.height, 8, 0, self.board.width + 2)

    def _restart(self):
        """Restart game with default values"""
        self.board = Board(10, 22)
        self.next_piece = random_tetromino(0, 0)
        self.current_piece = random_tetromino(5, 20)
        self.drop_time = .5
        self.current_key = -1
        self.lines_to_next_level = 15
        self.level = 1
        self.score = 0
        self.view_modified = True

    def process_messages(self):
        while not self.messages.empty():
            if self.messages.get() == "restart":
                self._restart()
                self.window.clear()

    def handle_user_input(self):
        direction = None
        key_pressed = self.window.getch()
        if key_pressed in (ord('j'), ord('J'), curses.KEY_LEFT):
            direction = Direction.Left
        elif key_pressed in (ord('l'), ord('L'), curses.KEY_RIGHT):
            direction = Direction.Right
        elif key_pressed in (ord('i'), ord('I'), curses.KEY_UP):
            direction = Direction.CCW
        elif key_pressed in (ord('k'), ord('K'), curses.KEY_DOWN):
            direction = Direction.CW
        elif key_pressed in (ord('q'), ord('Q')):
            self.view_modified = True
            game.switch_to_state("paused")
        elif key_pressed == ord(' '):
            self.drop_current_piece()

        if direction is not None:
            if direction == Direction.CCW or direction == Direction.CW:
                if self.board.are_valid_coordinates(
                        self.current_piece.rotate_result(direction)):
                    renderer.clear_tetromino(self.current_piece,
                                             self.board_window)
                    self.view_modified = True
                    self.current_piece.rotate(direction)
            else:
                if self.board.are_valid_coordinates(
                        self.current_piece.move_result(direction)):
                    renderer.clear_tetromino(self.current_piece,
                                             self.board_window)
                    self.view_modified = True
                    self.current_piece.move(direction)

    def drop_current_piece(self):
        self.view_modified = True
        renderer.clear_tetromino(self.current_piece, self.board_window)
        while self.board.are_valid_coordinates(
                self.current_piece.move_result(Direction.Down)):
            self.current_piece.move(Direction.Down)

    def draw(self):
        if self.view_modified:
            self.view_modified = False
            renderer.draw_board(self.board, self.board_window)
            renderer.draw_tetromino(self.current_piece, self.board_window)
            self.board_window.refresh()
            self._draw_info()

    def _draw_info(self):
        self.info_window.border()
        self.info_window.addstr(1, 1, "Tytrys")
        self.info_window.hline(2, 1, ord('_'), 6)
        self.info_window.addstr(4, 1, "Next:")
        self.next_piece.set_location(3, 14) # little hacky
        renderer.draw_tetromino(self.next_piece, self.info_window)
        self.info_window.addstr(10, 1, "Score:")
        self.info_window.addstr(11, 1, str(self.score))
        self.info_window.addstr(14, 1, "Level:")
        self.info_window.addstr(15, 3, str(self.level))
        self.info_window.addstr(18, 1, "Lines:")
        self.info_window.addstr(19, 1, str(self.lines_to_next_level) + "  ")
        self.info_window.refresh()

    def update(self, delta):
        self.elapsed_time += delta
        self.handle_user_input()

        if self.elapsed_time >= self.drop_time:
            if self.board.are_valid_coordinates(
                    self.current_piece.move_result(Direction.Down)):
                renderer.clear_tetromino(self.current_piece, self.board_window)
                self.current_piece.move(Direction.Down)
            else:
                renderer.clear_tetromino(self.next_piece, self.info_window)
                try:
                    self.board.lock_tetromino(self.current_piece)
                    self.current_piece = self.next_piece
                    self.current_piece.set_location(5, 20)
                    self.next_piece = random_tetromino(0, 0)

                    rows_removed = self.board.clear_full_rows()
                    if rows_removed:
                        self.lines_to_next_level -= rows_removed
                        self.score += sum(range(rows_removed + 1)) * 100
                        if self.lines_to_next_level <= 0:
                            self.score += 1000 * self.level
                            self.lines_to_next_level = 15
                            self.level += 1
                            self.drop_time *= .75
                except RuntimeError:
                    game.add_state_and_switch("game over",
                                              GameOverState(self.window,
                                                            self.score))

            self.view_modified = True
            self.elapsed_time -= self.drop_time


class MenuState(TytrysState):
    """Provides faculties for rendering menu in curses"""

    def __init__(self, window):
        super().__init__(window)
        self.choices = ()
        self.selected_choice = 0
        self.view_modified = True
        self.choice_changed = True
        self.line_to_start = 0
        self.lines_to_skip = 0

    def update(self, delta):
        key_press = self.window.getch()
        if key_press in (ord(' '), curses.KEY_ENTER, 10):
            self.choices[self.selected_choice][1]()
            self.choice_changed = True
            self.view_modified = True
        elif key_press in (ord('i'), ord('I'), curses.KEY_UP):
            self.selected_choice = (self.selected_choice - 1) % len(self.choices)
            self.choice_changed = True
        elif key_press in (ord('k'), ord('K'), curses.KEY_DOWN):
            self.selected_choice = (self.selected_choice + 1) % len(self.choices)
            self.choice_changed = True

    def draw(self):
        if self.view_modified:
            self.view_modified = False
            self.window.clear()
            self.window.border()

        if self.choice_changed:
            self.choice_changed = False
            self.draw_menu()

    def draw_menu(self):
        dimensions = self.window.getmaxyx()
        x_middle = dimensions[1] // 2
        for i, choice in enumerate(self.choices):
            self.window.addstr(
                self.line_to_start + (self.lines_to_skip * i),
                x_middle - len(choice[0]) // 2,
                choice[0],
                curses.A_REVERSE if i == self.selected_choice else curses.A_NORMAL)
        self.window.refresh()


class MainMenuState(MenuState):
    """Menu for home screen of game"""

    def __init__(self, window):
        super().__init__(window)
        self.choices = (("New Game", lambda: game.switch_to_state("game", "restart")),
                        ("Quit", lambda: game.switch_to_state("finished")))
        self.lines_to_skip = 4
        self.line_to_start = 10

    def draw(self):
        if self.view_modified:
            self.view_modified = False
            self.window.clear()
            self.window.border()
            self.window.addstr(6, 6, "TYTRYS!!!")

        if self.choice_changed:
            self.choice_changed = False
            self.draw_menu()


class PauseState(MenuState):
    """State the game enters when game is paused"""

    def __init__(self, window):
        super().__init__(window)
        self.choices = (("Continue", lambda: game.switch_to_state("game")),
                        ("Restart", lambda: game.switch_to_state("game", "restart")),
                        ("Quit", lambda: game.switch_to_state("finished")))
        self.lines_to_skip = 4
        self.line_to_start = 6


class GameOverState(MenuState):
    def __init__(self, window, score):
        super(GameOverState, self).__init__(window)
        self.score = score

        def start_new_game():
            game.remove_state("game over")
            game.switch_to_state("game", "restart")

        self.choices = (("New Game", start_new_game),
                        ("Quit", lambda: game.switch_to_state("finished")))
        self.lines_to_skip = 3
        self.line_to_start = 15

    def draw(self):
        if self.view_modified:
            self.view_modified = False
            self.window.clear()
            self.window.border()
            self.window.addstr(6, 1, "Game Over")
            self.window.addstr(10, 1, "Score: " + str(self.score))

        if self.choice_changed:
            self.choice_changed = False
            self.draw_menu()