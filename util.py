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

import adafruit_miniqr
import displayio
import terminalio

from adafruit_pybadger import pybadger


def display_bg_and_text(image, text=None, text_two=None):
    pybadger.show_business_card(
        image_name=image, email_string_one=text, email_string_two=text_two
    )


def generate_qr_code_display_group(url):
    """Generate and display a QR code for the given URL"""
    qr_code = adafruit_miniqr.QRCode(qr_type=2)
    qr_code.add_data(bytearray(url))
    qr_code.make()

    palette = displayio.Palette(2)
    palette[0] = 0xFFFFFF
    palette[1] = 0x000000

    qr_bitmap = pybadger.bitmap_qr(qr_code.matrix)
    qr_img = displayio.TileGrid(
        qr_bitmap, pixel_shader=palette, x=int(qr_bitmap.width / 2), y=2,
    )

    qr_code = displayio.Group(scale=3)
    qr_code.append(qr_img)

    qr_and_text_group = displayio.Group()
    qr_and_text_group.append(qr_code)
    qr_and_text_group.append(
        pybadger._create_label_group(
            text=url, font=terminalio.FONT, scale=1, height_adjustment=0.84
        )
    )
    return qr_and_text_group


PYTHON_BLUE = 0x4B8BBE
PYTHON_YELLOW = 0xFFD43B
CYAN = 0x0FF
PINK = 0xFF00FF
RED = 0xFF0000
ORANGE = 0xFF7F00
YELLOW = 0xFFFF00
GREEN = 0x00FF00
BLUE = 0x0000FF
INDIGO = 0x2E2B5F
VIOLET = 0x8B00FF

PYTHON_COLORS = [PYTHON_BLUE, PYTHON_YELLOW]
VAPORWAVE_COLORS = [CYAN, PINK]
RAINBOW_COLORS = [RED, ORANGE, YELLOW, GREEN, BLUE, INDIGO, VIOLET]

ALL_COLORS = PYTHON_COLORS + VAPORWAVE_COLORS + RAINBOW_COLORS
