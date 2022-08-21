# The *Potentiometer* Class

## Sample Setup

Note the Potentiometer output pin is connected to GPIO 28.

![Example Image](https://how2electronics.com/wp-content/uploads/2021/03/Raspberry-Pi-Pico-ADC-Example.jpg)

## Sample Usage

```python
from Potentiometer import Potentiometer as Poti
from time import sleep

poti = Poti(28)

while True:
    print(f"Raw: {poti.read_raw()}, Voltage: {poti.read_voltage()}V")
    sleep(0.5)

```

## Sample Output

```shell
Raw: 400, Voltage: 0.01933623V
Raw: 384, Voltage: 0.02094759V
Raw: 400, Voltage: 0.02094759V
Raw: 384, Voltage: 0.01933623V
```
