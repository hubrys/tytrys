import time
import queue

_states = {}
current_state = None
store = {}
finished = False
keyboard = None
_keyboard_function = None


def init():
    add_state("finished", Finished(None))


def set_keyboard_function(function):
    global _keyboard_function
    _keyboard_function = function


class Status(object):
    Running = 0
    Paused = 1
    Finished = 2
    Restart = 3


def add_state(identifier, state):
    global _states
    if isinstance(state, State):
        _states[identifier] = state


def remove_state(identifier):
    global _states
    del _states[identifier]


def switch_to_state(identifier, message=None):
    global _states
    global current_state
    if identifier in _states:
        current_state = _states[identifier]
        if message is not None:
            current_state.messages.put(message)
    else:
        raise StateIdentifierNotFoundError


def add_state_and_switch(identifier, state):
    add_state(identifier, state)
    switch_to_state(identifier)


def run():
    last = time.clock()
    while not finished:
        now = time.clock()  
        current_state.handle_messages()
        current_state.update(now - last)
        current_state.draw()
        last = now


class State(object):
    """
    defines a state that the game can be in
    """
    def __init__(self, window):
        self.status = Status.Running
        self.window = window
        self.elapsed_time = 0
        self.messages = queue.Queue()

    def handle_messages(self):
        pass

    def status(self):
        return self.status

    def update(self, delta):
        pass

    def draw(self):
        pass


class Finished(State):
    def update(self, delta):
        global finished
        finished = True


class StateIdentifierNotFoundError(Exception):
    pass