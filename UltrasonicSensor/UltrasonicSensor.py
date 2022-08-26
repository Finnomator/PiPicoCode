from machine import Pin, time_pulse_us
from time import sleep_us

__version__ = "0.1.0"
__author__ = "Finn Drünert"


class UltrasonicSensor:
    def __init__(
        self,
        trigger_pin: int,
        echo_pin: int,
        max_range_cm: float,
        trigger_input_signal_us: int = 10,
    ):
        self.trigger = Pin(trigger_pin, Pin.OUT, pull=None)
        self.echo = Pin(echo_pin, Pin.IN, pull=None)
        self.max_range_mm = int(max_range_cm * 10)
        self.echo_timeout_us = int(max_range_cm * 68.64)
        self.trigger_input_signal_us = trigger_input_signal_us
        self.trigger.off()

    def send_and_wait_for_pulse(self) -> int:

        """
        Returns the time the sound needs to get from trigger to echo in microseconds
        """

        self.trigger.off()
        sleep_us(5)
        self.trigger.on()
        sleep_us(self.trigger_input_signal_us)
        self.trigger.off()
        return time_pulse_us(self.echo, 1, self.echo_timeout_us)

    def get_distance_mm(self) -> int:
        mm = self.send_and_wait_for_pulse() * 1000000000000000 // 5827505827505828
        return mm if mm <= self.max_range_mm else -1
