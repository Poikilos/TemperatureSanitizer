#!/usr/bin/env python
from temper import Temper
t = Temper()
if hasattr(t, 'doctype'):
    # THIS IS BAD.
    print("You have the HTML templating engine, which has nothing to")
    print(" do with github.com/ccwienk/temper but has the same name.")
    exit(2)
elif hasattr(t, 'usb_devices'):
    print("You have the correct temper.")
    exit(0)
else
    print("Your temper package is ambiguous. It may either be the HTML template engine or the temperature sensor driver."
    exit(1)
