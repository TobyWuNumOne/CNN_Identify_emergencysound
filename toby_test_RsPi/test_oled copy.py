import os.path
from PIL import Image

from luma.core.interface.serial import i2c
from luma.oled.device import sh1106


def main():
    img_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "images", "A.png")
    )
    logo = Image.open(img_path).convert("RGBA")
    fff = Image.new(logo.mode, logo.size, (255,) * 4)

    background = Image.new("RGBA", device.size, "white")
    posn = ((device.width - logo.width) // 2, 0)

    while True:
        for angle in range(0, 360, 2):
            rot = logo.rotate(angle, resample=Image.BILINEAR)
            img = Image.composite(rot, fff, rot)
            background.paste(img, posn)
            device.display(background.convert(device.mode))


if __name__ == "__main__":
    try:
        serial = i2c(port=1, address=0x3C)
        device = sh1106(serial)
        main()
    except KeyboardInterrupt:
        pass
