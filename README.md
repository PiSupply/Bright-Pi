![Alt text](https://user-images.githubusercontent.com/1878314/73873874-60617180-484a-11ea-89c4-ff7867d7b396.png)
# Bright-Pi

The Bright-Pi is a small little board based around the [Semtech SC620](Documents/SC620.pdf) that powers 4 white LEDs and 8 infrared ones.

Please check our [quick start and FAQ](https://www.pi-supply.com/make/bright-pi-quickstart-faq/) for more information.

# Setup Bright-Pi

## Auto Installation

Just run the following script in a terminal window and Bright-Pi will be automatically setup.
```bash
# Run this line and Bright Pi will be setup and installed
curl -sSL https://pisupp.ly/brightpicode | bash
```

# Python API
The library provides two classes.
BrightPi provides driver functionalities for the SC620 whereas BrightPiSpecialEffects allows for an easier and more intuitive interface and usage.

## The Basic API

```python
# Global variables to quickly reference to groups of LEDs or individual ones.
# The LED* ones can only be used on their own.
LED_ALL = (1, 2, 3, 4, 5, 6, 7, 8)
LED_IR = LED_ALL[4:8]
LED_WHITE = LED_ALL[0:4]
LED1 = (1,)
LED2 = (2,)
LED3 = (3,)
LED4 = (4,)
LED5 = (5,)
LED6 = (6,)
LED7 = (7,)
LED8 = (8,)

ON = 1
OFF = 0

# reset method is used to reset the SC620 to its original state.
reset()

# get_gain and set_gain retrieve and set the gain for all LEDs.
get_gain()
# Gain from min 0 (0b0000) to max 15 (0b1111).
set_gain(gain)

# get_led_on_off and set_led_on_off retrieve and set the on/off status of the LEDs.
# White LEDs:
#   1, 2, 3, 4
# IR LEDs (in pairs)
#   5, 6, 7, 8
# leds is a tuple or array of LEDs for which you require a status.
get_led_on_off(leds)
# leds is a tuple or array of LEDs for which you are setting the status as state.
set_led_on_off(leds, state)

# get_dim and set_dim retrieve and set the dim for the specified LEDs.
get_led_dim()
# Dim from 0 (0x00) to 50 (0x32).
# leds is a tuple or array of LEDs for which you are setting the dimming level as dim.
set_led_dim(leds, dim)
```

## The Special Effects

```python
# Global variables to indicate clockwise and counterclockwise LEDs rotations sequences.
ROT_CW = 0
ROT_CCW = 1

# This method flashes all LEDs at an interval for a number of times.
# repetitions indicates how many flashes will be done and interval represents the time between on and off.
flash(repetitions, interval)

# This method flashes white LEDs top to bottom, left to right or from opposed sides.
# repetitions indicates how many flashes will be done and interval represents the time between on and off. Orientation defaults to 'v'.
# Allowed values are: 'v', 'h' and 'x'.
alt_flash(repetitions, interval, orientation)

# This method flashes one white LED after another as to give the impression of a rotating sequence.
# Using the global variables ROT_CW for clockwise and ROT_CCW for counterclockwise.
# repetitions indicates how many complete sequences will be done, delay represents the time between LEDs subsequently turning on and rotation set the direction.
night_rider(repetitions, delay, rotation)

# This method changes the gain on all LEDs from min (0b0000) to max (0b1111)
# repetitions indicates how many cycles will be done and speed represents how quickly each cycle will be completed by specifying a time between each change of gain.
beacon(repetitions, speed)

# This method changes the dimming on white LEDs from min (0x00) to max (0x32)
# repetitions indicates how many cycles will be done and speed represents how quickly each cycle will be completed by specifying a time between each change of dimming level.
dimmer(repetitions, speed)
```

### Examples

BrightPi

```python
from brightpi import *

brightPi = BrightPi()

# This method is used to reset the SC620 to its original state.
brightPi.reset()

# LEDs can be prepared as tuples by explicitly specifying each,
leds = (1, 2, 3, 4)
# or as an array,
leds = [1, 2]
# or by using global variables,
leds = LED_IR
brightPi.set_led_on_off(leds, OFF)
# global variables can be used in line,
brightPi.set_led_on_off(LED_WHITE, ON)
# and single LEDs can be used too.
brightPi.set_led_on_off(LED2, ON)

# When passing LEDs on their own without using the global variables each has to be represented as a tuple with only one element.
led1 = (1, )
brightPi.set_led_on_off(led1, ON)
# This could help for example in a loop.
for led in range(0, 8):
    brightPi.set_led_on_off((led + 1,), ON)
```

BrightPiSpecialEffects

```python
from brightpi import *

brightSpecial = BrightPiSpecialEffects()

# As BrightPiSpecialEffects inherits from BrighPi, managing the LEDs is done in the same way.
brightSpecial.set_led_on_off((1,), 0)

brightSpecial.set_led_on_off(LED4, 1)

brightSpecial.set_led_on_off((1,2,3,4), 1)

brightSpecial.set_led_on_off((1,2,3,4), 0)

# When using BrightPiSpecialEffects specific methods you will have to provide different parameters depending on the method chosen.
brightSpecial.beacon(2, 0.1)

# This method flashes one white LED after another as to give the impression of a clockwise rotating sequence.
brightSpecial.night_rider(10, 0.1)

# This method flashes one white LED after another as to give the impression of a counterclockwise rotating sequence.
brightSpecial.night_rider(10, 0.1, ROT_CCW)

brightSpecial.dimmer(2, 0.2)

brightSpecial.flash(5, 1)

# This method flashes white LEDs top to bottom.
brightSpecial.alt_flash(5, 0.2)

# This method flashes white LEDs left to right.
brightSpecial.alt_flash(5, 0.2, 'h')

# This method flashes white LEDs from opposed sides.
brightSpecial.alt_flash(5, 0.2, 'x')
```

# Command Line

```bash
# Run a demo using the various controls and effects
brightpi-test.py
```

# Hardware tips

**LED PN**
Bright Pi uses LEDs which are available off the shelf via a number of vendors.
The part numbers are:
* bright white LEDs (high quality Cree C513A-WSN-CV0Y0151 LEDs)
* bright IR LEDs (high quality LITEON HSDL-4261 LEDs)

**Pinout**
The Bright Pi header is connected to the Raspberry Pi via the GPIO header on pins:
```
GPIO              Bright Pi
2 - 5V       -->  2
3 - I2C_SDA  -->  4
4 - GND      -->  1
5 - I2C_SCL  -->  3
```
**NOTE:** The maximum current draw with all LEDs ON is 120mA.

# Third party software libraries

It is safe to say we have an awesome and growing community of people using Bright Pi to light up their projects and we get a huge amount of contributions of code, some of which we can easily integrate here and others which we can't (we are only a small team). However we want to make sure that any contributions are easy to find, for anyone looking. So here is a list of other software libraries that might be useful to you (if you have one of your own, please visit the ["Issues"](https://github.com/PiSupply/Bright-Pi/issues) tab above and let us know!):

* [Bright Pi Python Library from J Ritter](https://github.com/jritter/brightpi)

## Outdated documentation
[Code Examples](https://www.pi-supply.com/bright-pi-v1-0-code-examples/)

[Assembly guide](https://www.pi-supply.com/bright-pi-v1-0-assembly-instructions/)
