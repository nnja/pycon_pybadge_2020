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


class Credits(State):

    def display(self, pybadger):
        pybadger.show_business_card(
            image_name="images/credits.bmp",
        )

    def handle_event(self, pybadger):
        if any([
                pybadger.button.b,
                pybadger.button.start,
                pybadger.button.select]):
            menu.change_state(BadgeStates.MENU)


class NameBadge(State):

    def display(self, pybadger):
        pybadger.show_badge(
            name_string="Pythonista",
            hello_scale=2,
            my_name_is_scale=2,
            name_scale=2)

    def handle_event(self, pybadger):
        if any([
                pybadger.button.b,
                pybadger.button.start,
                pybadger.button.select]):
            menu.change_state(BadgeStates.MENU)


class QrCode(State):
    def display(self, pybadger):
        pybadger.show_qr_code(data="https://aka.ms/pycon2020")

    def handle_event(self, pybadger):
        if any([
                pybadger.button.b,
                pybadger.button.start,
                pybadger.button.select]):
            menu.change_state(BadgeStates.MENU)


class Menu(State):

    def __init__(self, menu_items):
        self.menu_items = menu_items
        self.current_index = 0
        self.buttons = []

        self.group = displayio.Group(max_size=5)

        display_height = 120
        step = int(display_height / len(self.menu_items))

        print("step is", step)

        for index, menu_item in enumerate(self.menu_items):
            button = Button(
                x=1, y=index * step, width=159, height=step,
                label_color=0xffff, outline_color=0x767676, fill_color=0x5c5b5c,
                selected_fill=0x5a5a5a, selected_outline=0xffff, selected_label=0xff00ff,
                label=menu_item, label_font=terminalio.FONT)
            if index == self.current_index:
                button.selected = True
            self.group.append(button.group)
            self.buttons.append(button)
        # TODO NZ max size here


    def display(self, pybadger):
        # TODO NZ highlight based on currently selected menu item
        print("Display Menu Here")
        pybadger.display.show(self.group)
        pybadger.display.refresh()

    def _change_highlighted_button(self):
        pass

    def handle_event(self, pybadger):
        if pybadger.button.a or pybadger.button.b or pybadger.button.select:
            menu.change_state(self.menu_items[self.current_index])
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
    MAIN_SCREEN = "Main Screen"
    MENU = "Menu"
    NAME_BADGE = "Name Badge"
    WEBSITE_QR_CODE = "Learn More"
    SOCIAL_BATTERY = "Social Battery Status"
    CREDITS = "Credits"
    EASTER_EGG = "Easter Egg"

    menu_items = [
        NAME_BADGE,
        WEBSITE_QR_CODE,
        SOCIAL_BATTERY,
        CREDITS,
        MAIN_SCREEN,
    ]

    states = {
        MAIN_SCREEN: PressStart(),
        MENU: Menu(menu_items),
        CREDITS: Credits(),
        NAME_BADGE: NameBadge(),
        WEBSITE_QR_CODE: QrCode(),
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
