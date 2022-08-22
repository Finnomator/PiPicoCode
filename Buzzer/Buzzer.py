from machine import Pin, PWM
from Morse import Morse
from time import sleep
from Pitches import Pitches

__version__ = "0.1.0"
__author__ = "Finn Drünert"


class ActiveBuzzer:
    def __init__(self, buzzer_pin: int):
        self.buzzer = Pin(buzzer_pin, Pin.OUT)
        self.buzzer.off()
        self.morse = Morse()

    def on(self):
        self.buzzer.on()

    def off(self):
        self.buzzer.off()

    def morse_dot(self):
        self.on()
        sleep(self.morse.dot_length)
        self.off()

    def morse_dash(self):
        self.on()
        sleep(self.morse.dash_length)
        self.off()

    def beep_morse(self, morse: str):
        for char in morse:
            if char == self.morse.dot:
                self.morse_dot()
            elif char == self.morse.dash:
                self.morse_dash()

            if char == self.morse.separator:
                sleep(self.morse.dash_length)
            elif char == self.morse.pause:
                sleep(self.morse.dash_length * 2)
            else:
                sleep(self.morse.dot_length)

    def beep_text_as_morse(self, text: str):
        self.beep_morse(self.morse.string_to_morse(text))


class PassiveBuzzer(Pitches):
    def __init__(self, buzzer_pin: int):
        super().__init__()
        self.buzzer = PWM(Pin(buzzer_pin, Pin.OUT))
        self.buzzer.freq(440)
        self.buzzer.duty_u16(2**12)

    def off(self):
        self.buzzer.duty_u16(0)

    def play_note(self, note: int, duration_ms: int):
        assert 30 < note < 4979
        self.buzzer.freq(note)
        sleep(duration_ms / 1000)

    def deinit(self):
        self.buzzer.deinit()
