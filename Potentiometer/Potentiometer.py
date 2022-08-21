from machine import ADC

__version__ = "0.1.0"
__author__ = "Finn Drünert"


class Potentiometer:
    def __init__(self, output_pin: int):
        self.poti = ADC(output_pin)
        self.conversion_factor = 3.3 / 65535

    def read_raw(self):
        return self.poti.read_u16()

    def read_voltage(self):
        return self.read_raw() * self.conversion_factor
