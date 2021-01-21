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


This program uses https://github.com/urwen/temper as a library, so
instead of calling temper.py which would run main, it does something
similar to what the main function of that file does.
'''


from temper import Temper
tmpr = Temper()
result = tmpr.read()
if len(result) < 1:
    print("temper didn't find any devices.")
    exit(1)
# print("result[0]['internal temperature']: {}".format(result[0]['internal temperature']))
print(result[0]['internal temperature'])
