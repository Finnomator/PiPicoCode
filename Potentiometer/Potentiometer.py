from machine import ADC

__version__ = "0.2.0"
__author__ = "Finn Drünert"


class Potentiometer(ADC):
    def __init__(self, output_pin: int):
        super().__init__(output_pin)
        self.conversion_factor_voltage = 3.3 / 65535
        self.conversion_factor_percent = 100 / 65535

    def read_voltage(self):
        return self.read_u16() * self.conversion_factor_voltage

    def read_percent(self):
        return self.read_u16() * self.conversion_factor_percent

    def read_range(self, value_range_lower: float = 0, value_range_upper: float = 1):
        assert (
            value_range_upper > value_range_lower
        ), "value_range_upper must be > value_range_lower"
        return value_range_lower + self.poti.read_u16() * (
            (value_range_upper - value_range_lower) / 65535
        )
