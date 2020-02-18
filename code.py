from adafruit_pybadger import PyBadger
import time
import displayio


class State():

    def display(self):
        raise NotImplementedError

    def handle_event(self):
        raise NotImplementedError


class PressStart(State):

    def display(self, pybadger):
        pybadger.show_business_card(
            image_name="images/initial.bmp",
            email_string_one="press start to begin"
        )

    def handle_event(self, pybadger):
        if pybadger.button.start:
            print("Start pressed!")
            menu.change_state(BadgeStates.MENU)


class Menu(State):

    menu_items = [
        "Name Badge",
        "Learn More",
        "Social Battery Status",
        "Credits",
        "Main Screen"
    ]

    def __init__(self):
        self.current_index = 0
        # TODO NZ max size here
        self.group = displayio.Group()

    def display(self, pybadger):
        # TODO NZ highlight based on currently selected menu item
        print("Display Menu Here")

    def handle_event(self, pybadger):
        if pybadger.button.up:
            print("Up button pressed")
            self.current_index = (self.current_index + 1) % len(self.menu_items)
            print("At item", self.menu_items[self.current_index])
        elif pybadger.button.down:
            print("Down button pressed")
            self.current_index = (self.current_index - 1) % len(self.menu_items)
            print("At item", self.menu_items[self.current_index])


class BadgeStates():
    MAIN_SCREEN = 0
    MENU = 1
    NAME_BADGE = 2
    WEBSITE_QR_CODE = 3
    SOCIAL_BATTERY = 4
    CREDITS = 5
    EASTER_EGG = 6

    states = {
        MAIN_SCREEN: PressStart(),
        MENU: Menu(),
    }

    current_state = MAIN_SCREEN

    def __init__(self, pybadger):
        self.pybadger = pybadger
        self.states[self.current_state].display(self.pybadger)

    def check_event(self):
        self.states[self.current_state].handle_event(self.pybadger)

    def change_state(self, new_state):
        # TODO NZ: clear display here?
        print("Changing state to", self.states[new_state].__class__)
        self.current_state = new_state
        self.states[self.current_state].display(self.pybadger)


pybadger = PyBadger()
menu = BadgeStates(pybadger)


while True:
    menu.check_event()
    time.sleep(0.2)  # Debounce
