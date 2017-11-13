![Alt text](https://user-images.githubusercontent.com/16068311/30545098-8eedf47e-9c80-11e7-9965-4d21b620abb1.png?raw=true "Bright Pi Logo")
# Bright-Pi

The Bright-Pi is a small little board based around the [Semtech SC620](https://www.google.co.uk/url?sa=t&rct=j&q=&esrc=s&source=web&cd=2&cad=rja&uact=8&ved=0ahUKEwiXn8rVrbzXAhVCCewKHXdPAnkQFggtMAE&url=http%3A%2F%2Fwww.semtech.com%2Fimages%2Fdatasheet%2Fsc620.pdf&usg=AOvVaw1Y8NLV9Bro2-hKjN3PcTvR) that powers 4 white LEDs and 8 infrared ones.
It is connected to the Raspberry Pi via the GPIO header on pins:
```
2 - 5V
3 - I2C_SDA
4 - GND
5 - I2C_SCL
```
Please check our [quick start and FAQ](https://www.pi-supply.com/make/bright-pi-quickstart-faq/) for more information.

# Setup Bright-Pi

## Auto Installation
_(URL not yet working)_

Just run the following script in a terminal window and PaPiRus will be automatically setup.
```bash
# Run this line and PaPiRus will be setup and installed
curl -sSL https://pisupp.ly/brightpicode | sudo bash
```

# Python API

## The Basic API

```python
from brightpi import *

brightPi = BrightPi()

brightPi.reset()

leds = LED_IR
brightPi.set_led_on_off(leds, OFF)
print(brightPi)

brightPi.set_led_on_off(LED_WHITE, ON)
print(brightPi)

brightPi.set_led_on_off(LED2, ON)

leds = [1, 2]
brightPi.set_led_on_off(leds, OFF)

for led in range(0, 8):
    brightPi.set_led_on_off((led + 1,), ON)
```

## The Special Effect

```python
from brightpi import *

brightSpecial = BrightPiSpecialEffects()

brightSpecial.set_led_on_off((1,), 0)

brightSpecial.set_led_on_off(LED4, 1)

brightSpecial.set_led_on_off((1,2,3,4), 1)

brightSpecial.set_led_on_off((1,2,3,4), 0)

brightSpecial.beacon(2, 0.1)

brightSpecial.reset()

brightSpecial.set_gain(8)

brightSpecial.nightRider(10, 0.1)

brightSpecial.nightRider(10, 0.1, ROT_CCW)

brightSpecial.dimmer(2, 0.2)

brightSpecial.flash(5, 1)

brightSpecial.altFlash(5, 0.2)

brightSpecial.altFlash(5, 0.2, 'h')

brightSpecial.altFlash(5, 0.2, 'x')
```

### Examples

# Hardware tips

# Third party software libraries

It is safe to say we have an awesome and growing community of people using Bright Pi to light up their projects and we get a huge amount of contributions of code, some of which we can easily integrate here and others which we can't (we are only a small team). However we want to make sure that any contributions are easy to find, for anyone looking. So here is a list of other software libraries that might be useful to you (if you have one of your own, please visit the ["Issues"](https://github.com/PiSupply/Bright-Pi/issues) tab above and let us know!):

* [Bright Pi Python Library from J Ritter](https://github.com/jritter/brightpi)

## Outdated documentation
[Code Examples](https://www.pi-supply.com/bright-pi-v1-0-code-examples/)

[Assembly guide](https://www.pi-supply.com/bright-pi-v1-0-assembly-instructions/) 