#!/usr/bin/env python

'''
This program checks the temperature for TEMPer USB devices supported by
the temper Python module, such as ones not supported by the temperusb
python module.

Such devices include usb id 413d:2107 (shown via the lsusb command with
no name beside it)
such as
["Temper High Accurate USB Thermometer Temperature Sensor Data Logger
Record for PC
Laptop"](https://www.amazon.com/gp/product/B009YRP906/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1)


This program uses ccwienk/temper https://github.com/ccwienk/temper as a
library (or any fork of the unmaintained urwen/temper), so instead of
calling temper.py which would run main, it does something similar to
what the main function of that file does.
'''

import sys
import getpass
user = getpass.getuser()
tryGroup = 'driverdev'


from temper import Temper
tmpr = Temper()
try:
    result = tmpr.read()
    scale = "C"
    for i in range(1, len(sys.argv)):
        arg = sys.argv[i]
        if arg == "-f":
            scale = "F"

    if len(result) < 1:
        print("temper didn't find any devices.")
        exit(1)
    # print("result[0]['internal temperature']: {}"
    # "".format(result[0]['internal temperature']))
    from tempermgr import c_to_f
    c = result[0]['internal temperature']
    t = c
    if scale.upper() == "F":
        t = c_to_f(c)
    print("{} {}".format(t, scale))
except PermissionError as ex:
    print("You must run with sudo, root, or add a udev rule via:")
    print('echo \'KERNEL=="hidraw*", SUBSYSTEM=="hidraw", MODE="0664",'
          ' GROUP="{}"\' | sudo tee /etc/udev/rules.d/'
          '99-hidraw-permissions.rules'.format(tryGroup))
    print('sudo usermod -a -G {} {}'.format(tryGroup, user))
    exit(3)
