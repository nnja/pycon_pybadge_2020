import time

import displayio
import terminalio

from adafruit_button import Button
from adafruit_display_text import label
from adafruit_pybadger import pybadger

from states import BadgeStates, DefaultMenuItemState, State
from util import ALL_COLORS, generate_qr_code_display_group, set_splash_screen


class PressStart(State):

    label = "Main Screen"

    def display(self):
        set_splash_screen(image="images/initial.bmp", text="press start to begin")

    def handle_event(self):
        if pybadger.button.start:
            state_manager.state = Menu
        elif pybadger.button.a and pybadger.button.b:
            state_manager.state = EasterEgg


class Credits(DefaultMenuItemState):

    label = "Credits"

    def display(self):
        set_splash_screen(image="images/credits.bmp")


class NameBadge(DefaultMenuItemState):

    label = "Name Badge"

    led_on = True
    colors = ALL_COLORS
    name = "Pythonista"

    def display(self):
        current_color = self.colors[self.current_index % len(self.colors)]
        pybadger.show_badge(
            name_string=self.name,
            background_color=current_color,
            hello_scale=2,
            my_name_is_scale=2,
            name_scale=2,
        )

        if self.led_on:
            pybadger.pixels.brightness = 0.1
            pybadger.pixels.fill(current_color)


class QrCode(DefaultMenuItemState):

    label = "Learn More"

    def display(self, url="https://aka.ms/pycon2020"):
        qr_group = generate_qr_code_display_group(url)
        pybadger.display.show(qr_group)


class SocialBattery(DefaultMenuItemState):

    label = "Social Battery Status"

    # TODO make this a named tuple
    social_images = [
        ("images/social_battery/full.bmp", (0, 255, 0)),
        ("images/social_battery/low.bmp", (255, 255, 0)),
        ("images/social_battery/empty.bmp", (255, 0, 0)),
    ]

    led_on = True

    def display(self):
        image_file, color = self.social_images[self.current_index % len(self.social_images)]
        pybadger.show_business_card(image_name=image_file)
        if self.led_on:
            pybadger.pixels.brightness = 0.1
            pybadger.pixels.fill(color)
        else:
            pybadger.pixels.fill((0, 0, 0))


class EasterEgg(State):

    label = "Easter Egg"

    def display(self):
        pybadger.show_business_card(image_name="images/easter_egg/easter_egg.bmp")
        # Wait 4 seconds, then return to main state_manager.
        time.sleep(4.0)
        state_manager.state = PressStart

# TODO: move this into states
class Menu(State):

    label = "Menu"

    menu_items = [
        NameBadge,
        SocialBattery,
        QrCode,
        Credits,
        PressStart,
    ]

    def __init__(self):
        self.current_index = 0
        self.buttons = []

        self.menu_group = displayio.Group(max_size=6)

        display_height = 120
        step = int(display_height / (len(self.menu_items) + 1))

        title = Button(
            x=1,
            y=0,
            width=159,
            height=step,
            label_color=0xFFFFFF,
            fill_color=0x000,
            label="Microsoft PyBadge v1.0",
            label_font=terminalio.FONT,
        )
        self.menu_group.append(title.group)

        for index, menu_item in enumerate(self.menu_items, start=1):
            button = Button(
                style=Button.ROUNDRECT,
                x=1,
                y=index * step,
                width=159,
                height=step,
                label_color=0xFFFF,
                outline_color=0x767676,
                fill_color=0x5C5B5C,
                selected_fill=0x5A5A5A,
                selected_outline=0xFF00FF,
                selected_label=0xFFFF00,
                label=menu_item.label,
                label_font=terminalio.FONT,
            )
            if index - 1 == self.current_index:
                button.selected = True
            self.menu_group.append(button.group)
            self.buttons.append(button)

    def display(self):
        pybadger.display.show(self.menu_group)
        pybadger.display.refresh()

    def handle_event(self):
        if pybadger.button.a:
            self.state_manager.state = self.menu_items[self.current_index]
        elif pybadger.button.b:
            self.state_manager.previous_state()
        elif pybadger.button.up or pybadger.button.down:
            self.buttons[self.current_index].selected = False
            if pybadger.button.up:
                self.current_index = (self.current_index - 1) % len(self.menu_items)
            elif pybadger.button.down:
                self.current_index = (self.current_index + 1) % len(self.menu_items)
            self.buttons[self.current_index].selected = True


state_manager = BadgeStates()
state_manager.add(
   PressStart(),
   Menu(),
   Credits(),
   NameBadge(),
   QrCode(),
   SocialBattery(),
   EasterEgg(),
)
state_manager.state = PressStart

while True:
    state_manager.check_for_event()
    time.sleep(0.15)  # Debounce
