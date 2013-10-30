from objects import Board, Square
import renderer
from renderer import Color


class Status(object):
    Created = 0
    Running = 1
    Finished = 2


class State(object):
    """
    defines a state that the game can be in
    """
    def __init__(self, window):
        self.status = Status.Created
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
        self.board_window = window.subwin(self.board.height+2, self.board.width + 2, 0, 0)
        self.current_piece = Square(4, 4)
        self.current_piece.color = Color.Blue

    def update(self, delta):
        self.elapsed_time += delta

    def draw(self):
        renderer.draw_board(self.board, self.board_window)
        renderer.draw_tetromino(self.current_piece, self.board_window)
        self.window.refresh()

