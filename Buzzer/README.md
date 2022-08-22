# The *Buzzer* Class

## Sample Setup

Make sure to get the polarity right.

![IMG](https://cdn.mos.cms.futurecdn.net/8iBtPr5NgxDomDjdWp2nRB.png)

## Sample Usage

### Active Buzzer

```python
from Buzzer import ActiveBuzzer
buz = ActiveBuzzer(15)

buz.beep_text_as_morse("Hello World!")
```

### Passive Buzzer

```python
from Buzzer import PassiveBuzzer
from Pitches import Pitches

buz = PassiveBuzzer(15)
for note in Pitches.ALL_NOTES:
    buz.play_note(note, 100)
buz.deinit()
```
