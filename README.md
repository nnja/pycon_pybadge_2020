
# Microsoft PyBadge at PyCon 2020

Adafruit PyBadges will be given away at the Microsoft booth at PyCon 2020 to attendees who stop by and complete hands-on labs.

This repository contains the initial code loaded on the badges.

To learn more about the badge and Microsoft at PyCon, please visit [https://aka.ms/pycon2020](https://aka.ms/pycon2020).

💜 Written by Nina Zakharenko ([@nnja](https://github.com/nnja)) with support from Luciana Abud ([@luabud](https://github.com/luabud)).

For more CircuitPython projects, stay in touch:
- [Twitter](https://twitter.com/nnja)
- [Twitch](https://www.twitch.tv/nnjaio) (watch live streamed coding and hardware projects)
- [dev.to](https://dev.to/nnja)
- [nnja.io](https://nnja.io)
- [GitHub](https://github.com/nnja)

## Getting Started

This code is meant to run on an Adafruit [PyBadge LC](https://www.adafruit.com/product/3939), a compact dev board featuring an ATSAMD51 processor, a color TFT screen with dimmable backlight, a wide assortment of buttons, and one NeoPixel LED.

It's written in [CircuitPython](https://circuitpython.org/), a variant of Python that can be used to program microcontrollers (Originally forked from [MicroPython](https://github.com/micropython/micropython))

To program the board, plug it into your computer with a micro USB cable that **supports data transfer**. *If you got your PyBadge from the Microsoft booth, use the USB cable from the kit.* Once you plug your board in, it should show up at a `CIRCUITPY` drive.

To change the behavior of the board, modify the code in `code.py`. Once it's saved, the latest code will run on the device automatically.

## The Badge

To get started from the main screen, press the "start" button on the upper right corner of the badge.

This will take you to the main menu.

### Main Menu

From the main menu, you can choose from the following options.

Press "a" to select, and "b" to go back.

#### Name Badge

Show your name, so everyone knows what to call you!

##### Name

Update the `NAME` constant at the top of the file with your own name.

##### Colors

Pass in the list of colors to the `NAME_BADGE_COLORS` constant at the top of the file. Colors can be hex values like `0xFF00FF` or a tuple of RGB values, like `(255, 0, 255)`.

Check `util.py` for color options.

Press the "left" and "right" buttons to switch between background colors.

##### LED

To turn the LED on, press the "up" button. To turn the LED off, press the "down" button. To make the LED off by default, change the value of `led_on` to `False` in the `NameBadge` class.

To change the brightness of the LED, increase the `LED_BRIGHTNESS` constant from 0.0 to 1.0.

#### Social Battery Status

Ever feel overwhelmed by large social gatherings and conferences? Now you can wear your social status on your badge!

The social statuses were originally created for [this project](https://twitter.com/nnja/status/1223854727005270018).

To switch your social status between Full, Low, and Empty, press the "left" and "right' buttons.

To turn the LED on, press the "up" button. To turn the LED off, press the "down" button. To make the LED off by default, change the value of `led_on` to `False` in the `SocialBattery` class.

#### Learn More

By default, this will show a QR code that leads to [https://aka.ms/pycon2020](https://aka.ms/pycon2020), where you can learn more about Microsoft and this project.

To change the QR code to your own site, change the `URL` constant at the top of the file.

#### Main Screen

Return to the main menu.

### Menu Items

#### Adding Menu Items

To add menu items, create a new class that inherits `DefaultMenuItemState`. Then, pass in your new class when instantiating the `MainMenu`, and add it to the `state_manager` by adding it to the list of states passed into `state_manager.add`.

#### Changing Menu Labels

To change the label of a menu item, update the `label` property on its class.

### Easter Egg

There's an surprise easter egg hidden in the code. Can you find it? 🥚📎✨

## CircuitPython and Libraries

### CircuitPython

This code targets CircuitPython version 5.0.0-beta.5. If you notice bugs or other issues with continued development, try to upgrade your board to the [latest version](https://circuitpython.org/board/pybadge/) by following [these instructions](https://learn.adafruit.com/adafruit-pybadge/installing-circuitpython).

### Libraries

This code depends on the [PyBadger](https://github.com/adafruit/Adafruit_CircuitPython_PyBadger/) library. [Version 2.0.0](https://github.com/adafruit/Adafruit_CircuitPython_PyBadger/tree/2.0.0) is included in the lib folder.

You may want to upgrade to the latest version. To upgrade your libraries, [download](https://circuitpython.org/libraries) the latest version for CircuitPython 5. Then, replace all the libraries in the `lib` folder from this bundle.

You may also want to read the [documentation](https://circuitpython.readthedocs.io/projects/pybadger/en/latest/), or view the source on [GitHub](https://github.com/adafruit/Adafruit_CircuitPython_PyBadger/).

## Editing the Code

I used [VS Code](https://code.visualstudio.com/download?WT.mc_id=pycon-github-ninaz) (an awesome IDE with [Python support](https://code.visualstudio.com/docs/languages/python?WT.mc_id=pycon-github-ninaz)) using the [Witch Hazel](https://marketplace.visualstudio.com/items?itemName=TheaFlowers.witch-hazel&WT.mc_id=pycon-github-ninaz) theme for the development of this code.
Follow these instructions for connecting to the serial port in the VS Code terminal to view printed output for [Mac/Linux](https://learn.adafruit.com/welcome-to-circuitpython/advanced-serial-console-on-mac-and-linux), and [Windows](https://learn.adafruit.com/welcome-to-circuitpython/advanced-serial-console-on-windows).

For programming hardware without an IDE [Mu](https://codewith.mu/) is a very simple text editor targeted for beginners.

## Contributions

This repository is meant to contain a snapshot of the code loaded on the badges at PyCon 2020. Minor fixes and version upgrades will be pushed, but new features will likely not be accepted.

If you make awesome modifications or add new features, please open an issue with a summary, a screenshot, and a link to your repository. Selected screenshots may be listed in a gallery in the future.

## License & Attributions

The code is published by Nina Zakharenko, and available under the [MIT License](https://github.com/nnja/pycon_pybadge_2020/blob/master/LICENSE).

#### Attributions

Background images are provided for customizing your badge in `images/backgrounds`.

Images:
- `Blinka.bmp` - Blinka the CircuitPython mascot from Adafruit
- `dog.bmp` - Photo by [Joe Caione](https://unsplash.com/@joeyc?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText) on [Unsplash](https://unsplash.com/)
- `flower.bmp` Photo by [Amy Shamblen](https://unsplash.com/@amyshamblen?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText) on [Unsplash](https://unsplash.com/)
- `weasel.bmp` - Photo by [Magalie St-Hialire Poulin](https://unsplash.com/@magaliiee13?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText) on [Unsplash](https://unsplash.com/)
- `moon.bmp` - Photo by [Nino Yang](https://unsplash.com/@ninoliverpool?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText) on [Unsplash](https://unsplash.com/)

Fonts used:
- [Sofia Font](https://www.fontsquirrel.com/fonts/sofia) by Latinotype