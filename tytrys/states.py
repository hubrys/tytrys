class Status(object):
    Created = 0
    Running = 1
    Finished = 2


class State(object):
    """
    defines a state that the game can be in
    """
    def __init__(self):
        self.status = Status.Created

    def start(self):
        """
        Called when state is first started, initialization code should go here
        """
        self.status = Status.Running

    def status(self):
        """
        Return status of state
        """
        return self.status

    def update(self, delta):
        """
        advances state delta seconds
        """
        pass

    def draw(self, window):
        """
        Draw self onto window
        """
        pass

    def exit(self):
        """
        Called when trying to exit, perform cleanup here
        """
        self.status = Status.Finished


class GameState(State):
    """
    state that actually plays the game
    """