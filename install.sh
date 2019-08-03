#!/usr/bin/env bash

# Enable I2C
sudo raspi-config nonint do_i2c 0

# Install python-smbus if not installed
sudo apt-get install git python3-smbus python3-distutils -y

git clone https://github.com/PiSupply/Bright-Pi.git

cd Bright-Pi

sudo python3 setup.py install

whiptail --msgbox "The system will now reboot" 8 40
sudo reboot
