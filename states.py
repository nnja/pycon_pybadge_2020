from adafruit_pybadger import pybadger


class State:

    label = "State"

    def __init__(self):
        self.state_manager = None

    def display(self):
        raise NotImplementedError

    def handle_event(self):
        raise NotImplementedError


class DefaultMenuItemState(State):

    led_on = False

    def __init__(self):
        self.current_index = 0
        super().__init__()

    def should_return_to_menu(self, buttons):
        return any([buttons.b, buttons.start, buttons.select])

    def handle_event(self):
        buttons = pybadger.button
        if self.should_return_to_menu(buttons):
            pybadger.pixels.fill((0, 0, 0))  # Turn off neopixels
            self.state_manager.previous_state()
        elif pybadger.button.up:
            if hasattr(self, "led_on"):
                self.led_on = True
                self.display()
        elif pybadger.button.down:
            if hasattr(self, "led_on"):
                self.led_on = False
                pybadger.pixels.fill((0, 0, 0))
        elif pybadger.button.left or pybadger.button.right:
            if pybadger.button.left:
                self.current_index -= 1
            elif pybadger.button.right:
                self.current_index += 1
            self.display()


class BadgeStates:
    current_state = None

    def __init__(self):
        self.states = {}
        self._previous_states = []

    def add(self, *states):
        for state in states:
            state.state_manager = self

        self.states.update({state.__class__: state for state in states})

    def previous_state(self):
        if self._previous_states:
            self.current_state = self._previous_states.pop()
            self.states[self.current_state].display()

    def check_for_event(self):
        self.states[self.current_state].handle_event()

    @property
    def state(self):
        return self.states[self.current_state]

    @state.setter
    def state(self, state):
        print("Changing state to", self.states[state].__class__)
        self._previous_states.append(self.current_state)
        self.current_state = state
        self.states[self.current_state].display()
