class State():

    def display(self):
        raise NotImplementedError

    def handle_event(self):
        raise NotImplementedError


class DefaultMenuItemState(State):

    def decrease_index(self, collection):
        if hasattr(self, "current_index"):
            self.current_index = (self.current_index - 1) % len(collection)

    def increase_index(self, collection):
        if hasattr(self, "current_index"):
            self.current_index = (self.current_index + 1) % len(collection)

    def handle_event(self, pybadger):
        buttons = pybadger.button
        if any([
                buttons.b,
                buttons.start,
                buttons.select]):
            pybadger.pixels.fill((0, 0, 0))  # Turn off neopixels
            menu.change_state(BadgeStates.MENU)
        elif pybadger.button.up:
            if hasattr(self, "led_on"):
                self.led_on = True
                self.display(pybadger)
        elif pybadger.button.down:
            if hasattr(self, "led_on"):
                self.led_on = False
                pybadger.pixels.fill((0, 0, 0))


class BadgeStates():
    MAIN_SCREEN = "Main Screen"
    MENU = "Menu"
    NAME_BADGE = "Name Badge"
    WEBSITE_QR_CODE = "Learn More"
    SOCIAL_BATTERY = "Social Battery Status"
    CREDITS = "Credits"
    EASTER_EGG = "Easter Egg"

    current_state = MAIN_SCREEN

    def set_initial_states(self, states):
        self.states = states

    def set_pybadger(self, pybadger):
        self.pybadger = pybadger
        if self.states:
            self.states[self.current_state].display(self.pybadger)
        else:
            print("Please set states first.")

    def check_for_event(self):
        self.states[self.current_state].handle_event(self.pybadger)

    def change_state(self, new_state):
        print("Changing state to", self.states[new_state].__class__)
        self.current_state = new_state
        self.states[self.current_state].display(self.pybadger)


menu = BadgeStates()
