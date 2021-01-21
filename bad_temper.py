#!/usr/bin/env python
from temper import Temper
silent_if_ok = False
import sys
for i in range(1, len(sys.argv)):
    arg = sys.argv[i]
    if arg == "--silent-if-ok":
        silent_if_ok = True
    else:
        print("Unknown argument: {}".format(arg))
        exit(6)

t = Temper()
if hasattr(t, 'doctype'):
    # THIS IS BAD.
    print("You have the HTML templating engine, which has nothing to")
    print(" do with github.com/ccwienk/temper but has the same name.")
    exit(2)
elif hasattr(t, 'usb_devices'):
    if not silent_if_ok:
        print("You have the correct temper.")
    exit(0)
else:
    print("Your temper package is ambiguous. It may either be the HTML template engine or the temperature sensor driver.")
    exit(5)
