# The *Ultrasonic Sencor* Class

In this example we will be using the HC-SR04 Ultrasonic Sensor.

## Ultrasonic Ranging Module HC - SR04

### Image

![Img](https://m.media-amazon.com/images/I/816Znr0INNL._SX342_.jpg)

### Specifications

|Property|Value|
|---|---|
|Working Voltage|DC 5V|
|Working Current|15mA|
|Working Frequency|40Hz|
|**Max Range**|**4m**|
|Min Range|2cm|
|MeasuringAngle|15 degree|
|**Trigger Input Signal**|**10uS TTL pulse**|
|Echo Output Signal|Input TTL lever signal and the range in proportion|
|Dimension |45\*20\*15mm|

## Sample Setup

The sensor runs with 5V and 15mA which has to be regulated with about 120Ω (exactly 112Ω) to 3.3V in order to ground it on the Pi.
Also the echo pin should be protected by a 1kΩ resistor.

![Img](USSampleImage.jpg)

### Connections

|Sensor Pin|GPIO|
|---|---|
|Echo|14|
|Trigger|15|

## Sample Code

Note that we use the `max_range_cm` and `trigger_input_signal_us` given in the specifications table.

```python
from UltrasonicSensor import UltrasonicSensor as US
from time import sleep

us = US(trigger_pin=15, echo_pin=14, max_range_cm=400, trigger_input_signal_us=10)

while True:
    distance_mm = us.get_distance_mm()
    print(f"Distance: {distance_mm}mm ({distance_mm//10}cm)")
    sleep(0.5)

```
