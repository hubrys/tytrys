
from objects import Board, Square, Direction, random_tetromino
import curses
import renderer
from renderer import Color


class Status(object):
    Running = 0
    Finished = 1


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
        self.board = Board(10, 22)
        self.board_window = window.subwin(self.board.height, self.board.width + 2, 0, 0)
        self.debug_window = window.subwin(0, 35)
        self.next_piece = random_tetromino(5, 20)
        self.current_piece = random_tetromino(5, 20)
        self.drop_time = 1000
        self.current_key = -1
        self.lines = 0

    def update(self, delta):
        self.elapsed_time += delta
        self.get_user_input()
        self.handle_user_input()

        if self.elapsed_time >= self.drop_time:
            if self.board.are_valid_coordinates(
                    self.current_piece.move_result(Direction.Down)):
                self.current_piece.move(Direction.Down)
                self.window.clear()
            else:
                self.board.lock_tetromino(self.current_piece)
                self.current_piece = self.next_piece
                self.next_piece = random_tetromino(5, 20)
                rows_removed = self.board.clear_full_rows()
                if rows_removed:
                    self.lines += rows_removed
                    self.window.clear()

            self.elapsed_time -= self.drop_time

        self.draw()

    def get_user_input(self):
        self.current_key = self.window.getch()

    def handle_user_input(self):
        direction = None
        if self.current_key == ord('j'):
            direction = Direction.Left
        elif self.current_key == ord('l'):
            direction = Direction.Right
        elif self.current_key == ord('q'):
            self.status = Status.Finished
        if direction is not None:
            if self.board.are_valid_coordinates(
                    self.current_piece.move_result(direction)):
                self.current_piece.move(direction)
                self.board_window.clear()

    def draw(self):
        renderer.draw_board(self.board, self.board_window)
        renderer.draw_tetromino(self.current_piece, self.board_window)
        self.board_window.refresh()
        self.debug_info()

    def debug_info(self):
        window = self.debug_window
        window.border()

        window.addstr(1, 1, "Board Dimensions: (" + str(self.board.width) + ", " + str(self.board.height) + ")")
        window.addstr(2, 1, "Piece Coordinates: ")
        for i, coordinate in enumerate(self.current_piece.coordinates):
            window.addstr(3 + i, 1, "\t\t(" + str(coordinate.x) + ", " + str(coordinate.y) + ")")

        window.addstr(7, 1, "Elapsed Time: " + str(self.elapsed_time))
        window.addstr(8, 1, "Lines Cleared: " + str(self.lines))
        window.refresh()