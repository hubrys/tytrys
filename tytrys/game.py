import time
import queue

_states = {}
current_state = None
store = {}
finished = False
keyboard = None
_keyboard_function = None


def init():
    """initialize game state"""
    # For now it just adds the finished state to _states
    add_state("finished", Finished())


def run():
    """Start game loop

    Calls methods of current state while game.finished is not false

    """
    last = time.clock()
    while not finished:
        now = time.clock()
        current_state.process_messages()
        current_state.update(now - last)
        current_state.draw()
        last = now


class Status(object):
    """Defines state constants"""
    Running = 0
    Paused = 1
    Finished = 2
    Restart = 3


def add_state(identifier, state):
    """Add state to game, making it available with switch_to_state

    Arguments:
    identifier -- identifier for state
    state -- state to add

    Raises:
    StateIdentifierAlreadyExistsError
        if state already exists for identifier

     """
    global _states
    if identifier in _states:
        raise StateIdentifierAlreadyExistsError(
            "State for identifier " + str(identifier) + "already exists"
        )

    if not isinstance(state, State):
        raise TypeError("given argument is not an instance of game.State")

    _states[identifier] = state


def remove_state(identifier):
    """Remove state associated with identifier from state list

    Arguments:
    identifier -- identifier of state to remove

    """
    global _states
    del _states[identifier]


def switch_to_state(identifier, message=None):
    """Switch to state associated with identifier with optional message"

    Arguments:
    identifier -- identifier of state to switch to
    message (optional) -- message to pass to state

    """
    global _states
    global current_state

    if identifier not in _states:
        raise StateIdentifierNotFoundError

    current_state = _states[identifier]
    if message is not None:
        current_state.messages.put(message)
        # give state a chance to handle messages before taking over
    current_state.process_messages()


def add_state_and_switch(identifier, state):
    """Add state to state list and make current

    Arguments:
    identifier -- identifier for state
    state -- state to add

    Equivalent to calling:
        add_state(identifier, state)
        switch_to_state(identifier, state)

    """
    add_state(identifier, state)
    switch_to_state(identifier)


class State(object):
    """Defines a state that the game can be in"""

    def __init__(self):
        """Initialize basic state"""
        self.status = Status.Running
        self.messages = queue.Queue()

    def send_message(self, message):
        pass

    def process_messages(self):
        """Process messages received"""
        pass

    def status(self):
        """Return status of state as Status"""
        return self.status

    def update(self, delta):
        """Advance state by delta seconds

        Arguments:
        delta -- time to advance state forward through

        """
        pass

    def draw(self):
        """Draw state

        Default implementation does nothing

        """
        pass


class Finished(State):
    """State for indicating that game has finished"""
    def update(self, delta):
        global finished
        finished = True


class StateIdentifierNotFoundError(Exception):
    """Raised when identifier cannot be found in state list"""
    pass


class StateIdentifierAlreadyExistsError(Exception):
    """Raised when identifier is already associated with identifier"""
    pass