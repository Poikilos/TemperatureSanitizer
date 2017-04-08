#!/usr/bin/env python
#region User Settings
desired_degrees = 120
desired_format = "fahrenheit"
interval_seconds = 60
desired_total_seconds = 120 * 60
#endregion User Settings

settings_howto_msg="#These settings are in the TemperatureSanitizer.py file in the User Settings region."

import time
try:
    from temperusb import TemperDevice, TemperHandler
except:
    print("You do not have temperusb installed.\n"
          "Please run the following commands in terminal\n"
          " (if in Windows first cd C:\Python27 [or your Python folder],\n"
          " but if in *nix-like environment first sudo su -):\n"
          "python -m pip install --upgrade pip\n"
          "python -m pip install --upgrade pip wheel\n"
          "python -m pip install temperusb\n")
    exit(1)
th = None
try:
    th = TemperHandler()
except:
    print("A TEMPerV1 compatible device is not plugged in, or you have no permission to the usb device. Try running this script with sudo (sudo python TemperatureSanitizer.py) or search online for linux usb permissions.")
    exit(2)
tds = th.get_devices()
current_span_temperatures_count = 0
current_span_temperatures_total_temperature = 0


class TSBake:
    def __init__(self):
        self.temperatures = list()
        self.total_seconds = 0
        self.warmup_seconds = None

complete_bakes = list()
incomplete_bakes = list()

current_bake = TSBake()
current_temperatures = list()
warmup_seconds = 0
if (len(tds)>0):
    print("interval_seconds: "+str(interval_seconds))
    print("desired_degrees: "+str(desired_degrees))
    print("desired_format: "+str(desired_format))
    print("#Bake starts after desired_degrees is reached:")
    print("desired_bake_seconds: "+str(desired_total_seconds))
    print("#desired_bake_minutes: "+str(desired_total_seconds/60))
    print("")
    print("#This program will show minimum temperature every "+str(interval_seconds)+" second(s), whether that span's minimum met (>=) the desired minimum, and will tell you after the temperature has been the desired minimum of "+str(desired_degrees)+" "+desired_format+" for any continuous stretch of "+str(desired_total_seconds/60)+" minutes"+".")
    print(settings_howto_msg)
    print("#Please wait...")
    while (True):
        this_temp = tds[0].get_temperature(format=desired_format)
        current_span_temperatures_count += 1
        current_span_temperatures_total_temperature += this_temp
        current_temperatures.append(this_temp)
        if current_span_temperatures_count >= interval_seconds:
            this_avg = current_span_temperatures_total_temperature / current_span_temperatures_count
            this_min = min(current_temperatures)
            del current_temperatures[:]
            met_msg = "(< "+str(desired_degrees)+") "
            if (this_min >= desired_degrees):
                current_bake.temperatures.append(this_min)
                current_bake.total_seconds += current_span_temperatures_count
                met_msg = "(>= "+str(desired_degrees)+") "
                if (current_bake.total_seconds>=desired_total_seconds):
                    complete_bakes.append(current_bake)
                    current_bake = TSBake()
                    current_bake.warmup_seconds = warmup_seconds
            else:
                if len(current_bake.temperatures) > 0:
                    if (current_bake.total_seconds<desired_total_seconds):
                        incomplete_bakes.append(current_bake)
                        current_bake = TSBake()
                        current_bake.warmup_seconds = warmup_seconds
                    else:
                        print("#Logic error detected (this should never happen): program did not end when bake was successful (appending bake to complete_bakes anyway).")
                        complete_bakes.append(current_bake)
                        current_bake = TSBake()
                        current_bake.warmup_seconds = warmup_seconds
                    
            print("#"+met_msg+"Last "+str(current_span_temperatures_count)+" second(s) average:"+str(this_avg)+"; minimum:"+str(this_min))
            current_span_temperatures_count = 0
            current_span_temperatures_total_temperature = 0
            if (len(complete_bakes)>0):
                print("#Baking is finished: ")
                break
        time.sleep(1)
        warmup_seconds += 1

    print("incomplete_bakes:")
    for stretch in incomplete_bakes:
        print("  - minimum_temperatures: "+str(stretch.temperatures))
        print("    warmup_time_minutes: "+str(stretch.warmup_seconds/60))
        print("    bake_minutes: "+str(stretch.total_seconds/60))
    print("complete_bakes:")
    for stretch in complete_bakes:
        print("  - minimum_temperatures: "+str(stretch.temperatures))
        print("    warmup_time_minutes: "+str(stretch.warmup_seconds/60))
        print("    bake_minutes: "+str(stretch.total_seconds/60))
    print("incomplete_bakes_count: "+str(len(incomplete_bakes)))
    print("complete_bakes_count: "+str(len(complete_bakes)))
    print("")

else:
    print("No TEMPer device found.")
