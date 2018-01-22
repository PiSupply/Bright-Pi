#!/usr/bin/env bash

# Enable I2C
raspi-config nonint do_i2c 0

git clone --depth=1 https://github.com/PiSupply/BrightPi.git

cd Bright-Pi

python setup.py install

whiptail --msgbox "The system will now reboot" 8 40
reboot
