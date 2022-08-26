# The *RGB Led Class*

## Sample Setup

![IMG](https://i1.wp.com/www.pibits.net/wp-content/uploads/2021/01/pico-and-rgb-led_bb.jpg)

### Connections

|RGB Led pin|GPIO|
|---|---|
|red|16|
|green|18|
|blue|20|

## Sample Code

```python
from RGBLed import RGBLed

rgb_led = RGBLed(red_led=16, green_led=18, blue_led=20)

rgb_led.color_cicle(color_cicles=10)
rgb_led.deinit()
```
