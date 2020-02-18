from adafruit_pybadger import PyBadger
import time
import displayio
from adafruit_button import Button
import terminalio

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
        "Main Screen",
    ]

    def __init__(self):
        self.current_index = 0
        self.buttons = []
        # TODO NZ max size here


    def display(self, pybadger):
        # TODO NZ highlight based on currently selected menu item
        print("Display Menu Here")
        self.group = displayio.Group(max_size=5)

        step = int(pybadger.display.height / len(self.menu_items))

        print("step is", step)

        for index, menu_item in enumerate(self.menu_items):
            button = Button(
                x=1, y=index * step, width=160, height=step,
                label_color=0xff7e00, outline_color=0x767676, fill_color=0x5c5b5c,
                selected_fill=0x5a5a5a, selected_outline=0xff6600, selected_label=0xffff,
                label=menu_item, label_font=terminalio.FONT)
            if index == self.current_index:
                button.selected = True
            self.group.append(button.group)
            self.buttons.append(button)

        pybadger.display.show(self.group)
        pybadger.display.refresh()

    def _change_highlighted_button(self):
        pass

    def handle_event(self, pybadger):
        if pybadger.button.a or pybadger.button.b or pybadger.button.select:
            pass
        if pybadger.button.up:
            self.buttons[self.current_index].selected = False
            print("Up button pressed")
            self.current_index = (self.current_index - 1) % len(self.menu_items)
            print("At item", self.menu_items[self.current_index])
            self.buttons[self.current_index].selected = True
        elif pybadger.button.down:
            self.buttons[self.current_index].selected = False
            print("Down button pressed")
            self.current_index = (self.current_index + 1) % len(self.menu_items)
            print("At item", self.menu_items[self.current_index])
            self.buttons[self.current_index].selected = True


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
    time.sleep(0.15)  # Debounce
