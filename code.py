from adafruit_pybadger import PyBadger
import time
import displayio
from adafruit_button import Button
import terminalio
import adafruit_miniqr


class State():

    def display(self):
        raise NotImplementedError

    def handle_event(self):
        raise NotImplementedError


class DefaultMenuItemState(State):

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


class PressStart(State):

    def display(self, pybadger):
        pybadger.show_business_card(
            image_name="images/initial.bmp",
            email_string_one="press start to begin"
        )

    def handle_event(self, pybadger):
        if pybadger.button.start:
            menu.change_state(BadgeStates.MENU)
        elif pybadger.button.a and pybadger.button.b:
            menu.change_state(BadgeStates.EASTER_EGG)


class Credits(DefaultMenuItemState):

    def display(self, pybadger):
        pybadger.show_business_card(
            image_name="images/credits.bmp",
        )


class NameBadge(DefaultMenuItemState):

    colors = [
        # Python Colors
        0x4B8BBE,   # Python Blue
        0xFFD43B,   # Python Yellow
        # Vaporwave Colors
        0x0ff,      # Cyan
        0xff00ff,   # Pink
        # Rainbow Colors
        0xff0000,   # Red
        0xFF7F00,   # Orange
        0xFFFF00,   # Yellow
        0x00FF00,   # Green
        0x0000FF,   # Blue
        0x2E2B5F,   # Indigo,
        0x8B00FF,   # Violet,
    ]

    current_index = 0
    led_on = False

    def display(self, pybadger):
        current_color = self.colors[self.current_index]
        pybadger.show_badge(
            background_color=current_color,
            name_string="Pythonista",
            hello_scale=2,
            my_name_is_scale=2,
            name_scale=2
        )

        if self.led_on:
            pybadger.pixels.brightness = 0.1
            pybadger.pixels.fill(current_color)

    def handle_event(self, pybadger):
        if pybadger.button.left:
            print("Left button pressed")
            self.current_index = (self.current_index - 1) % len(self.colors)
            self.display(pybadger)
        elif pybadger.button.right:
            print("Right button pressed")
            self.current_index = (self.current_index + 1) % len(self.colors)
            self.display(pybadger)
        super().handle_event(pybadger)


class QrCode(DefaultMenuItemState):

    def display(self, pybadger, url = "https://aka.ms/pycon2020"):
        qr_code = adafruit_miniqr.QRCode(qr_type=2)
        qr_code.add_data(bytearray(url))
        qr_code.make()

        palette = displayio.Palette(2)
        palette[0] = 0xFFFFFF
        palette[1] = 0x000000

        qr_bitmap = pybadger.bitmap_qr(qr_code.matrix)
        qr_img = displayio.TileGrid(
            qr_bitmap,
            pixel_shader=palette,
            x=int(qr_bitmap.width / 2),
            y=2,
        )

        qr_code = displayio.Group(scale=3)
        qr_code.append(qr_img)

        qr_and_text_group = displayio.Group()
        qr_and_text_group.append(qr_code)
        qr_and_text_group.append(
            pybadger._create_label_group(
                text=url,
                font=terminalio.FONT,
                scale=1,
                height_adjustment=0.84)
        )
        pybadger.display.show(qr_and_text_group)


class SocialBattery(DefaultMenuItemState):

    social_images = [
        ("images/social_battery/full.bmp", (0, 255, 0)),
        ("images/social_battery/low.bmp", (255, 255, 0)),
        ("images/social_battery/empty.bmp", (255, 0, 0)),
    ]

    current_index = 0

    def display(self, pybadger):
        image_file, color = self.social_images[self.current_index]
        pybadger.show_business_card(
            image_name=image_file
        )
        pybadger.pixels.brightness = 0.1
        pybadger.pixels.fill(color)

    def handle_event(self, pybadger):
        if pybadger.button.left:
            print("Left button pressed")
            self.current_index = (self.current_index - 1) % len(self.social_images)
            self.display(pybadger)
        elif pybadger.button.right:
            print("Right button pressed")
            self.current_index = (self.current_index + 1) % len(self.social_images)
            self.display(pybadger)
        super().handle_event(pybadger)


class EasterEgg(State):

    def display(self, pybadger):
        pybadger.show_business_card(
            image_name="images/easter_egg/easter_egg.bmp"
        )
        # Wait 4 seconds, then return to main menu.
        time.sleep(4.0)
        menu.change_state(BadgeStates.MAIN_SCREEN)


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
        print("Display Menu Here")
        pybadger.display.show(self.group)
        pybadger.display.refresh()

    def _change_highlighted_button(self):
        pass

    def handle_event(self, pybadger):
        if pybadger.button.a or pybadger.button.select:
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
        SOCIAL_BATTERY: SocialBattery(),
        EASTER_EGG: EasterEgg(),
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
