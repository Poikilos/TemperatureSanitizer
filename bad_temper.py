#!/usr/bin/env python
from temper import Temper
t = Temper()
if hasattr(t, 'doctype'):
    # THIS IS BAD.
    print("You have the HTML parser, which has nothing to do with")
    print("but has the same name.")
    exit(2)
