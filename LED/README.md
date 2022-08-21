# The *LED* Class

## Sample Setup

Note the LED is connected to GPIO 15.

![IMG](https://projects-static.raspberrypi.org/projects/getting-started-with-the-pico/725a421f3b51a5674c539d6953db5f1892509475/en/images/single_LED.png)

## Sample Usage

```python
from LED import LED
from time import sleep

led = LED(15)

led.on()  # Sets the LED brightness to 100%
sleep(1)
led.off()  # Sets the LED brightness to 0%
sleep(1)
led.value_percent(50)  # Sets the LED brightness to 50%
sleep(1)
led.value(49151)  # Sets the LED brightness to 75%
sleep(1)

# Lets the LED slowly brighten and dim again
# The smaller update_delay is, the faster the LED will change in brightness
led.value_gradient(mode=LED.INCREASE_DECREASE, update_delay=0.0001)

```
