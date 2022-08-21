import time
from machine import Pin, PWM

__version__ = "0.1.0"
__author__ = "Finn Drünert"


class LED:

    INCREASE = 0
    DECREASE = 1
    INCREASE_DECREASE = 2
    DECREASE_INCREASE = 3

    def __init__(self, led_pin: int):
        self.pwm_led = PWM(Pin(led_pin, Pin.OUT))
        self.pwm_led.freq(1000)
        self.pwm_led.duty_u16(0)

    def off(self):
        self.pwm_led.duty_u16(0)

    def on(self):
        self.pwm_led.duty_u16(65535)

    def value_percent(self, percent: float):
        """
        Set the led brightness in percent
        percent: 0 <= percent <= 100
        """

        assert 0 <= percent <= 100, "Percent musst be between [0, 100]"

        self.pwm_led.duty_u16(int(65535 * (percent / 100)))

    def value(self, value: int):
        """
        Set the led brightness
        value: 0 <= value <= 65535
        """

        assert type(value) is int, "Value must be an int"

        self.pwm_led.duty_u16(value)

    def value_gradient(self, mode: int = INCREASE, update_delay: float = 0.0001):

        if mode == self.INCREASE_DECREASE:
            mode = self.DECREASE
            self.value_gradient(self.INCREASE, update_delay)
        elif mode == self.DECREASE_INCREASE:
            mode = self.INCREASE
            self.value_gradient(self.DECREASE, update_delay)
        elif mode > 3:
            raise Exception("Invalid mode")

        start = 0 if mode == self.INCREASE else 65535
        end = 65535 if mode == self.INCREASE else -1
        inv = 1 if mode == self.INCREASE else -1
        for i in range(start, end, inv):
            self.pwm_led.duty_u16(i)
            time.sleep(update_delay)
