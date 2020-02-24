# MIT License

# Copyright (c) 2020 Nina Zakharenko

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import displayio
import terminalio

from adafruit_button import Button
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
    _led_color = None

    def __init__(self):
        self.current_index = 0
        super().__init__()

    @property
    def led_color(self):
        return self._led_color

    @led_color.setter
    def led_color(self, led_color):
        self._led_color = led_color
        if self.led_on and self._led_color:
            pybadger.pixels.fill(self._led_color)

    def should_return_to_menu(self, buttons):
        return any([buttons.b, buttons.start, buttons.select])

    def handle_event(self):
        buttons = pybadger.button
        if self.should_return_to_menu(buttons):
            pybadger.pixels.fill((0, 0, 0))  # Turn off neopixels
            self.state_manager.previous_state()
        elif pybadger.button.up:
            self.led_on = True
            self.display()
        elif pybadger.button.down:
            self.led_on = False
            pybadger.pixels.fill((0, 0, 0))
        elif pybadger.button.left or pybadger.button.right:
            if pybadger.button.left:
                self.current_index -= 1
            elif pybadger.button.right:
                self.current_index += 1
            self.display()


class MainMenu(State):

    label = "Menu"

    def __init__(self, *menu_items):
        self.menu_items = menu_items
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


class StateManager:
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
