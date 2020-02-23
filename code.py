import time

import displayio
from adafruit_pybadger import pybadger
from states import BadgeStates, DefaultMenuItemState, MainMenu, State
from util import ALL_COLORS, generate_qr_code_display_group, set_splash_screen


class PressStart(State):

    label = "Main Screen"

    def display(self):
        set_splash_screen(image="images/initial.bmp", text="press start to begin")

    def handle_event(self):
        if pybadger.button.start:
            state_manager.state = MainMenu
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
        image_file, color = self.social_images[
            self.current_index % len(self.social_images)
        ]
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


main_menu = MainMenu(NameBadge, SocialBattery, QrCode, Credits, PressStart)

state_manager = BadgeStates()
state_manager.add(
    main_menu,
    PressStart(),
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
