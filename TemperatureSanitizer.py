#!/usr/bin/env python

from __future__ import print_function

try:
    input = raw_input
except NameError:
    # Python 3
    pass

from tempermgr import TemperMgr

settings_howto_msg = (
    "# These settings are in the TemperatureSanitizer.py file and\n"
    "# can be passed to the TemperMgr constructor as a dict."
)
import datetime
import time

def callback(msg):
    print(msg)

def main():
    mgr = TemperMgr()
    print("interval: {}".format(mgr.get("interval")))
    print("target: {}".format(mgr.get('target')))
    print("scale: {}".format(mgr.get('scale')))
    print("# {} starts after target temperature is reached:"
          "".format(mgr.process_term))
    ptl = mgr.process_term.lower()
    print("minTime{}: {}"
          "".format(ptl, mgr.get("minTime")))
    print("#minTime{}_minutes: {}"
          "".format(ptl, mgr.get("minTime")/60))
    print("")
    print("#This program will show minimum temperature every "
          + str(mgr.get("interval")) + " second(s), whether that span's"
          " minimum met (>=) the desired minimum, and will tell you"
          " after the temperature has been the desired minimum of "
          + str(mgr.get('target')) + " " + mgr.get('scale')
          + " met continuously for {}".format(mgr.get("minTime")/60)
          + " minutes" + ".")
    print(settings_howto_msg)
    print("start_datetime: {}".format(datetime.datetime.now()))
    #try:
    print("#nominal_device_reading: {}".format(mgr.getTemp()))
    '''
    except:
        print("#Could not finish reading temperature from the device.")
        exit(3)
    '''
    print("#Please wait...")
    while (True):
        try:
            mgr.iterate(callback=callback)
        except StopIteration:
            break
        time.sleep(1)
        mgr.warmTime += 1

    print("incomplete_{}s:".format(ptl))
    for bake in mgr.incomplete_bakes:
        print("  - minimum_temperatures: {}".format(bake.temperatures))
        print("    pre{}_minutes: {}"
              "".format(ptl, bake.warmTime/60))
        print("    {}_minutes: {}"
              "".format(ptl, bake.time/60))
    print("complete_{}s:".format(ptl))
    for bake in mgr.complete_bakes:
        print("  - minimum_temperatures: {}".format(bake.temperatures))
        print("    pre{}_time_minutes: {}"
              "".format(ptl, bake.warmTime/60))
        print("    {}_minutes: {}"
              "".format(ptl, bake.time/60))
    print("incomplete_{}s_count: {}"
          "".format(ptl, len(mgr.incomplete_bakes)))
    print("complete_{}s_count: {}"
          "".format(ptl, len(mgr.complete_bakes)))
    print("end_datetime: {}".format(datetime.datetime.now()))
    print("")


    input("Press enter to exit")

if __name__ == "__main__":
    main()
