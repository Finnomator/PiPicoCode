from machine import Pin, PWM
from LED import LED
from time import sleep

__version__ = "0.1.0"
__author__ = "Finn Drünert"


class RGB:
    def rgb_to_hsv(self, r: float, g: float, b: float):
        """
        0 <= r <= 1
        0 <= g <= 1
        0 <= b <= 1
        returns h between 0 and 360, s, v between 0 and 1
        """

        assert 0 <= r <= 1 and 0 <= g <= 1 and 0 <= b <= 1

        cmax = max(r, g, b)
        cmin = min(r, g, b)
        diff = cmax - cmin

        if cmax == cmin:
            h = 0
        elif cmax == r:
            h = (60 * ((g - b) / diff) + 360) % 360
        elif cmax == g:
            h = (60 * ((b - r) / diff) + 120) % 360
        elif cmax == b:
            h = (60 * ((r - g) / diff) + 240) % 360
        if cmax == 0:
            s = 0
        else:
            s = diff / cmax

        v = cmax
        return h, s, v

    def hsv_to_rgb(self, h: float, s: float, v: float):

        """
        0 <= h <= 360
        0 <= s <= 1
        0 <= v <= 1
        returns three floats (r, g, b) between 0 and 1
        """

        assert 0 <= h <= 360 and 0 <= s <= 1 and 0 <= v <= 1

        hi = h // 60

        f = h / 60 - hi

        p = v * (1 - s)
        q = v * (1 - s * f)
        t = v * (1 - s * (1 - f))

        if hi == 0 or hi == 6:
            r, g, b = v, t, p
        elif hi == 1:
            r, g, b = q, v, p
        elif hi == 2:
            r, g, b = p, v, t
        elif hi == 3:
            r, g, b = p, q, v
        elif hi == 4:
            r, g, b = t, p, v
        elif hi == 5:
            r, g, b = v, p, q

        return r, g, b


class RGBLed(RGB):
    def __init__(self, red_led: LED | int, green_led: LED | int, blue_led: LED | int):
        self.red = red_led if type(red_led) is LED else LED(red_led)
        self.green = green_led if type(green_led) is LED else LED(green_led)
        self.blue = blue_led if type(blue_led) is LED else LED(blue_led)

        self.leds = [self.red, self.green, self.blue]

    def __infinity(self):
        i = 0
        while True:
            yield i
            i += 1

    def set_values(self, r: int, g: int, b: int):
        self.red.value(r)
        self.green.value(g)
        self.blue.value(b)

    def color_cicle(
        self, color_cicles: int = -1, update_delay: float = 0.0001, step_size: int = 8
    ):
        """
        color_cicles: -1 == infinte
        update_delay: time to wait after each color change
        step_size: one cicle == range(0, 65536, step_size)
        """

        assert color_cicles >= -1, "color_cicles must be >= -1"

        for _ in range(color_cicles) if color_cicles != -1 else self.__infinity():
            for i in range(0, 65536, step_size):
                r, g, b = self.hsv_to_rgb(360 * (i / 65535), 1, 1)
                self.set_values(int(r * 65535), int(g * 65535), int(b * 65535))
                sleep(update_delay)

    def deinit(self):
        for led in self.leds:
            led.off()
            sleep(0.001)
            led.deinit()
