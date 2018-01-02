#!/usr/bin/env bash

# Enable I2C
raspi-config nonint do_i2c 0

git clone https://github.com/PiSupply/Bright-Pi.git

whiptail --msgbox "The system will now reboot" 8 40
reboot
