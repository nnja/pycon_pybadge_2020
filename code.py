from adafruit_pybadger import PyBadger
import time


class Action():

    def display(self):
        # TODO NZ: clear display here?
        raise NotImplementedError

    def handle_event(self):
        raise NotImplementedError


class PressStart(Action):

    def display(self, pybadger):
        pybadger.show_business_card(
            image_name="images/initial.bmp", email_string_one="press start to begin"
        )

    def handle_event(self, pybadger):
        if pybadger.button.start:
            print("Start pressed!")
            menu.change_state(BadgeMenu.MENU)


class Menu(Action):

    def display(self, pybadger):
        print("Display Menu Here")

    def handle_event(self, pybadger):
        if pybadger.button.a:
            print("Button A pressed")


class BadgeMenu():
    START = PressStart()
    MENU = Menu()
    # NAME_BADGE = 2
    # QR_CODE = 3
    # EXPOVERT = 4
    # THANKS = 5
    # EASTER_EGG = 6

    current_state = START

    def __init__(self, pybadger):
        self.pybadger = pybadger
        self.current_state.display(self.pybadger)

    def check_event(self):
        self.current_state.handle_event(self.pybadger)

    def change_state(self, new_state):
        print("Changing state to", new_state.__class__)
        self.current_state = new_state


pybadger = PyBadger()
menu = BadgeMenu(pybadger)


while True:
    menu.check_event()
    time.sleep(0.5)  # Debounce
