#!/usr/bin/env python

from distutils.core import setup
from brightpi import brightpilib

setup(name="brightpi",
      version=brightpilib.__version__,
      description="BrightPi API",
      author='PiSupply',
      author_email='sales@pi-supply.com',
      url='pi-supply.com',
      packages=['brightpi'],
      scripts=['src/brightpi-test.py']
      )
