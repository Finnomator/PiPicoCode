# The *Potentiometer* Class

This class is made to convert the raw `ADC.read_u16()` output to units like volts.

## Sample Setup

Note the Potentiometer output pin is connected to GPIO 28.

![Example Image](https://how2electronics.com/wp-content/uploads/2021/03/Raspberry-Pi-Pico-ADC-Example.jpg)

## Sample Usage

```python
from Potentiometer import Potentiometer as Poti
from time import sleep

poti = Poti(28)

while True:
    raw = poti.read_u16()
    sleep(0.01)
    percentage = poti.read_percent()
    sleep(0.01)
    volt = poti.read_voltage()
    sleep(0.01)
    custom = poti.read_range(0, 255)  # e.g. RGB Value
    print(f"{raw=}, {percentage=}%, {volt=}V, {custom=}")
    sleep(0.5)
```

## Sample Output

```shell
raw=48491, percentage=72.99153%, volt=2.39583V, custom=186.8755
raw=48107, percentage=73.65072%, volt=2.417583V, custom=186.3152
raw=46379, percentage=70.52567%, volt=2.353129V, custom=180.463
raw=16083, percentage=24.27253%, volt=0.7929366V, custom=60.08949
raw=20517, percentage=32.03937%, volt=1.10564V, custom=93.71595
```
