__version__ = "2.0"
# This software is designed to work with Bright Pi
# https://www.pi-supply.com/product/bright-pi-bright-white-ir-camera-light-raspberry-pi/
# Special thanks to jritter for his original work on brightpi https://github.com/jritter/brightpi

# White LEDs:
#   1, 2, 3, 4
# IR LEDs (in pairs)
#   5, 6, 7, 8
# Gain from 0 to 15
# Dim from 0 to 50

import smbus
import time

# Global variables to quickly reference to groups of LEDs or individual ones.
# The LED* ones can only be used on their own
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
ROT_CW = 0
ROT_CCW = 1

class BrightPi:
    _device_address = 0x70
    _gain_register = 0x09
    _led_status_register = 0x00
    _max_dim = 0x32
    _max_gain = 0b1111
    _default_gain = 0b1000
    # LEDs are reordered so that 0..3 are white and 4..7 are IR pairs
    _led_hex = (0x02, 0x08, 0x10, 0x40, 0x01, 0x04, 0x20, 0x80)
    _led_dim_hex = (0x02, 0x04, 0x05, 0x07, 0x01, 0x03, 0x06, 0x08)

    def __init__(self):
        # Attributes are set by reading the SC620 state
        self._bus = smbus.SMBus(1)
        self._led_on_off = self._bus.read_byte_data(BrightPi._device_address, BrightPi._led_status_register)
        self._led_dim = [0 for i in range(0, 8)]
        for i in range(0, 8):
            self._led_dim[i] = self._bus.read_byte_data(BrightPi._device_address, i + 1)
        self._gain = self._bus.read_byte_data(BrightPi._device_address, BrightPi._gain_register)

    def __str__(self):
        # Provide a comma separated output for further manipulation
        return "{},{},{}".format(self._gain, self._led_on_off, tuple(self._led_dim))

    def reset(self):
        # This method is used to reset the SC620 to its original state
        self.set_gain(BrightPi._default_gain)
        self.set_led_dim(LED_ALL, BrightPi._max_dim)
        self.set_led_on_off(LED_ALL, OFF)

    def get_gain(self):
        return self._gain

    def set_gain(self, gain):
        if gain >= 0 and gain <= BrightPi._max_gain:
            self._gain = gain
            self._bus.write_byte_data(BrightPi._device_address, BrightPi._gain_register, self._gain)

    def get_led_on_off(self, leds):
        # The status of the LEDs is returned as an array where an ON LED is represented with numbers from 1 to 8 depending on its position in _led_hex
        # An OFF LED is represented with a 0
        led_states = [OFF for i in range(0, 8)]
        led_reg_states = self._bus.read_byte_data(BrightPi._device_address, BrightPi._led_status_register)
        for led in leds:
            if led >= 1 and led <= 8:
                if led_reg_states & self._led_hex[led - 1]:
                    led_states[led - 1] = led
        return led_states

    def set_led_on_off(self, leds, state):
        if state == ON or state == OFF:
            for led in leds:
                if led >= 1 and led <= 8:
                    self._led_on_off = self._bus.read_byte_data(BrightPi._device_address, BrightPi._led_status_register)
                    if state == ON:
                        self._led_on_off = self._led_on_off | BrightPi._led_hex[led - 1]
                    else:
                        self._led_on_off = self._led_on_off & ~ BrightPi._led_hex[led - 1]
                self._bus.write_byte_data(BrightPi._device_address, BrightPi._led_status_register, self._led_on_off)

    def get_led_dim(self):
        return self._led_dim

    def set_led_dim(self, leds, dim):
        if dim >= 0 and dim <= BrightPi._max_dim:
            for led in leds:
                if led >= 1 and led <= 8:
                    self._led_dim[led - 1] = dim
                    self._bus.write_byte_data(BrightPi._device_address, self._led_dim_hex[led - 1], self._led_dim[led - 1])

class BrightPiSpecialEffects(BrightPi):
    # This class provides a further level of abstraction to allow for easier usage
    def __init__(self):
        super(BrightPiSpecialEffects, self).__init__()

    def __str__(self):
        # The output is provides a readable format of the Bright Pi's status
        return "Gain: {}\nLED Status:{}\nLED Dimming:{}".format(self.get_gain(), tuple(self.get_led_on_off(LED_ALL)), tuple(self.get_led_dim()))

    def flash(self, repetitions, interval):
        # This method flashes all LEDs at an interval for a number of times
        for rep in range(0, repetitions):
            self.set_led_on_off(LED_ALL, ON)
            time.sleep(interval)
            self.set_led_on_off(LED_ALL, OFF)
            time.sleep(interval)

    def alt_flash(self, repetitions, interval, orientation ='v'):
        # This method flashes white LEDs top to bottom, left to right or from opposed sides
        for rep in range(0, repetitions):
            if orientation == 'v':
                self.set_led_on_off((1, 2), ON)
                self.set_led_on_off((3, 4), OFF)
                time.sleep(interval)
                self.set_led_on_off((1, 2), OFF)
                self.set_led_on_off((3, 4), ON)
                time.sleep(interval)
            elif orientation == 'h':
                self.set_led_on_off((1, 3), ON)
                self.set_led_on_off((2, 4), OFF)
                time.sleep(interval)
                self.set_led_on_off((1, 3), OFF)
                self.set_led_on_off((2, 4), ON)
                time.sleep(interval)
            elif orientation == 'x':
                self.set_led_on_off((1, 4), ON)
                self.set_led_on_off((2, 3), OFF)
                time.sleep(interval)
                self.set_led_on_off((1, 4), OFF)
                self.set_led_on_off((2, 3), ON)
                time.sleep(interval)
            else:
                print("Wrong parameter for orientation")

    def night_rider(self, repetitions, delay, rotation = ROT_CW):
        # This method flashes one white LED after another as to give the impression of a rotating sequence
        # Using the global variables ROT_CW for clockwise and ROT_CCW for counterclockwise
        if rotation == ROT_CW:
            for rep in range(0, repetitions):
                for i in range(1, 5):
                    self.set_led_on_off((i,), ON)
                    time.sleep(delay)
                    self.set_led_on_off((i,), OFF)
        elif rotation == ROT_CCW:
            for rep in range(0, repetitions):
                for i in range(4, 0, -1):
                    self.set_led_on_off((i,), ON)
                    time.sleep(delay)
                    self.set_led_on_off((i,), OFF)
        else:
            print("Wrong parameter for rotation")

    def beacon(self, repetitions, speed):
        # This method changes the gain on all LEDs from min (0b0000) to max (0b1111)
        self.set_led_on_off(LED_ALL, ON)
        for rep in range(0, repetitions):
            for gain in range(0, 16):
                self.set_gain(gain)
                time.sleep(speed)
            for gain in range(15, -1, -1):
                self.set_gain(gain)
                time.sleep(speed)

    def dimmer(self, repetitions, speed):
        # This method changes the dimmming on white LEDs from min (0x00) to max (0x32)
        self.set_led_on_off(LED_ALL, ON)
        for rep in range(0, repetitions):
            for dim in range(0, 50):
                self.set_led_dim(LED_WHITE, dim)
                time.sleep(speed)
            for dim in range(49, -1, -1):
                self.set_led_dim(LED_WHITE, dim)
                time.sleep(speed)
