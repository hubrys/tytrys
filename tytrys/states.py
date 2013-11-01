from objects import Board, Square, Direction, random_tetromino
import curses
import renderer
from renderer import Color


class Status(object):
    Running = 0
    Paused = 1
    Finished = 2
    Restart = 3


class State(object):
    """
    defines a state that the game can be in
    """

    def __init__(self, window):
        self.status = Status.Running
        self.window = window
        self.elapsed_time = 0

    def status(self):
        return self.status

    def update(self, delta):
        pass


class GameState(State):
    """
    state that actually plays the game
    """

    def __init__(self, window):
        super().__init__(window)
        #These lines are so that I don't have to stare at warnings, restart sets these to the right values
        self.board = Board(10, 22)
        self.next_piece = random_tetromino(0, 0)
        self.current_piece = random_tetromino(5, 20)
        self.drop_time = .5
        self.current_key = -1
        self.lines_to_next_level = 1
        self.level = 1
        self.score = 0
        self.view_modified = True

        self.restart()
        self.board_window = window.derwin(self.board.height, self.board.width + 2, 0, 0)
        self.info_window = window.derwin(self.board.height, 8, 0, self.board.width + 2)

    def restart(self):
        self.board = Board(10, 22)
        self.next_piece = random_tetromino(0, 0)
        self.current_piece = random_tetromino(5, 20)
        self.drop_time = .5
        self.current_key = -1
        self.lines_to_next_level = 1
        self.level = 1
        self.score = 0
        self.view_modified = True

    def get_user_input(self):
        self.current_key = self.window.getch()

    def handle_user_input(self):
        direction = None
        if self.current_key in (ord('j'), ord('J'), curses.KEY_LEFT):
            direction = Direction.Left
        elif self.current_key in (ord('l'), ord('L'), curses.KEY_RIGHT):
            direction = Direction.Right
        elif self.current_key in (ord('i'), ord('I'), curses.KEY_UP):
            direction = Direction.CCW
        elif self.current_key in (ord('k'), ord('K'), curses.KEY_DOWN):
            direction = Direction.CW
        elif self.current_key in (ord('q'), ord('Q')):
            self.status = Status.Paused
        elif self.current_key == ord(' '):
            self.drop_current_piece()
        if direction is not None:
            if direction == Direction.CCW or direction == Direction.CW:
                if self.board.are_valid_coordinates(self.current_piece.rotate_result(direction)):
                    renderer.clear_tetromino(self.current_piece, self.board_window)
                    self.view_modified = True
                    self.current_piece.rotate(direction)
            else:
                if self.board.are_valid_coordinates(self.current_piece.move_result(direction)):
                    renderer.clear_tetromino(self.current_piece, self.board_window)
                    self.view_modified = True
                    self.current_piece.move(direction)

    def drop_current_piece(self):
        self.view_modified = True
        renderer.clear_tetromino(self.current_piece, self.board_window)
        while self.board.are_valid_coordinates(self.current_piece.move_result(Direction.Down)):
            self.current_piece.move(Direction.Down)

    def draw(self):
        if self.view_modified:
            self.view_modified = False
            renderer.draw_board(self.board, self.board_window)
            renderer.draw_tetromino(self.current_piece, self.board_window)
            self.board_window.refresh()
            self.draw_info()

    def draw_info(self):
        self.info_window.border()
        self.info_window.addstr(1, 1, "Tytrys")
        self.info_window.hline(2, 1, ord('_'), 6)
        self.info_window.addstr(4, 1, "Next:")
        self.next_piece.set_location(3, 14)
        renderer.draw_tetromino(self.next_piece, self.info_window)
        self.info_window.addstr(10, 1, "Score:")
        self.info_window.addstr(11, 1, str(self.score))
        self.info_window.addstr(14, 1, "Level:")
        self.info_window.addstr(15, 3, str(self.level))
        self.info_window.addstr(18, 1, "Lines:")
        self.info_window.addstr(19, 1, str(self.lines_to_next_level))

    def update(self, delta):
        self.elapsed_time += delta
        self.get_user_input()
        self.handle_user_input()

        if self.elapsed_time >= self.drop_time:
            if self.board.are_valid_coordinates(self.current_piece.move_result(Direction.Down)):
                renderer.clear_tetromino(self.current_piece, self.board_window)
                self.view_modified = True
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
                    self.restart()
                    #self.status = Status.Restart

            self.view_modified = True
            self.elapsed_time -= self.drop_time

        self.draw()


class PauseState(State):
    """
    state the game enters when game is paused

    breaks the point of the state as its easier to stop looping and handle events
    """
    def __init__(self, window):
        super().__init__(window)
        self.choices = (("Continue", Status.Running),
                        ("Restart", Status.Restart),
                        ("Quit", Status.Finished))
        self.selected_choice = 0

    def update(self, delta):
        self.window.nodelay(0)
        self.window.clear()
        while True:
            self.draw_choices()
            key_press = self.window.getch()
            if key_press in (ord(' '), curses.KEY_ENTER, 10):
                self.status = self.choices[self.selected_choice][1]
                break
            elif key_press in (ord('i'), ord('I'), curses.KEY_UP):
                self.selected_choice = (self.selected_choice - 1) % len(self.choices)
            elif key_press in (ord('k'), ord('K'), curses.KEY_DOWN):
                self.selected_choice = (self.selected_choice + 1) % len(self.choices)
        self.window.nodelay(1)
        self.window.clear()

    def draw_choices(self):
        dimensions = self.window.getmaxyx()
        x_middle = dimensions[1] // 2
        y_middle = dimensions[0] // 2
        step = 4
        for i, choice in enumerate(self.choices):
            self.window.addstr(
                y_middle + (step * (i - 1)),
                x_middle - len(choice[0]) // 2,
                choice[0],
                curses.A_REVERSE if i == self.selected_choice else curses.A_NORMAL)
        self.window.refresh()