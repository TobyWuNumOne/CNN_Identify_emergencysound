#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014-17 Richard Hull and contributors
# See LICENSE.rst for details.
# PYTHON_ARGCOMPLETE_OK

"""
Display the Raspberry Pi logo (loads image as .png).
"""
import time
import os.path
from PIL import Image

from luma.core.interface.serial import i2c, spi
from luma.oled.device import ssd1306, ssd1325, ssd1331, sh1106


def main():
    while True:
        img_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "images", "A(2).png")
        )
        logo = Image.open(img_path).convert("RGBA")
        background = Image.new("RGBA", device.size, "black")
        posn = ((device.width - logo.width) // 2, 0)
        background.paste(logo, posn)
        device.display(background.convert(device.mode))
        time.sleep(1)
        device.clear()


if __name__ == "__main__":
    try:
        serial = i2c(port=1, address=0x3C)
        device = sh1106(serial)
        main()
    except KeyboardInterrupt:
        pass
