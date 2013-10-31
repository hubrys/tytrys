from objects import Board, Square, Direction, random_tetromino
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
        self.board = Board(30, 40)
        self.board_window = window.subwin(self.board.height + 2, self.board.width + 2, 0, 0)
        self.debug_window = window.subwin(0, 35)
        self.next_piece = random_tetromino(20, 20)
        self.current_piece = random_tetromino(20, 20)
        self.drop_time = 4000

        self.board.rows[0] = [Color.Red, None]*15

    def update(self, delta):
        self.elapsed_time += delta
        self.debug_info()

        if self.elapsed_time >= self.drop_time:
            if self.board.are_valid_coordinates(self.current_piece.move_result(Direction.Down)):
                self.current_piece.move(Direction.Down)
                self.window.clear()
            else:
                self.board.lock_tetromino(self.current_piece)
                self.current_piece = self.next_piece
                self.next_piece = random_tetromino(20, 20)
                # todo: check to see if next piece is allowed.
            self.elapsed_time -= self.drop_time

        self.draw()

    def draw(self):
        renderer.draw_board(self.board, self.board_window)
        renderer.draw_tetromino(self.current_piece, self.board_window)
        self.board_window.refresh()

    def debug_info(self):
        window = self.debug_window
        window.border()

        window.addstr(1, 1, "Board Dimensions: (" + str(self.board.width) + ", " + str(self.board.height) + ")")
        window.addstr(2, 1, "Piece Coordinates: ")
        for i, coordinate in enumerate(self.current_piece.coordinates):
            window.addstr(3 + i, 1, "\t\t(" + str(coordinate.x) + ", " + str(coordinate.y) + ")")

        window.addstr(7, 1, "Elapsed Time: " + str(self.elapsed_time))
        window.refresh()



