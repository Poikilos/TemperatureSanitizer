#!/usr/bin/env python

#region User Settings
desired_degrees = 120
desired_format = "fahrenheit"
interval_seconds = 60
desired_total_seconds = 120 * 60
desired_comparison = ">="
desired_collate_method = "average"
#endregion User Settings

opposite_operator = dict()
opposite_operator["<"] = ">="
opposite_operator["<="] = ">"
opposite_operator[">"] = "<="
opposite_operator[">="] = "<"

process_term = "Bake"
if desired_comparison in ["<=","<"]:
    process_term = "Chill"
    if desired_collate_method in ["max","maximum"]:
        print("# WARNING: using min or average is recommended for chill, \n" +
              "#   but "+desired_collate_method+" was selected")


def is_criteria_met(temperatures):
    global desired_degrees
    global desired_comparison
    global desired_collate_method
    result = None
    operand = None
    if desired_collate_method in ["min","minimum"]:
        operand = min(temperatures)
    elif desired_collate_method in ["max","maximum"]:
        operand = max(temperatures)
    elif desired_collate_method in ["avg","average"]:
        operand = sum(temperatures) / float(len(temperatures))
    else:
        print("# Unknown collate method was selected. Please use: \n" +
              "#   min, max, or average")
        exit(5)
    met_enable = False
    if desired_comparison == ">=":
        met_enable = (operand >= desired_degrees)
    elif desired_comparison == ">":
        met_enable = (operand > desired_degrees)
    elif desired_comparison == "<=":
        met_enable = (operand <= desired_degrees)
    elif desired_comparison == "<":
        met_enable = (operand < desired_degrees)
    else:
        print("# Unknown comparison was selected. Please use: \n" +
              "#   <, <=, >, or >=")
        exit(6)
    if met_enable:
        result = operand
    return result
    

settings_howto_msg="#These settings are in the TemperatureSanitizer.py file in the User Settings region."
import datetime
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
    print("#"+process_term+" starts after desired_degrees is reached:")
    print("desired_"+process_term.lower()+"_seconds: "+str(desired_total_seconds))
    print("#desired_"+process_term.lower()+"_minutes: "+str(desired_total_seconds/60))
    print("")
    print("#This program will show minimum temperature every "+str(interval_seconds)+" second(s), whether that span's minimum met (>=) the desired minimum, and will tell you after the temperature has been the desired minimum of "+str(desired_degrees)+" "+desired_format+" met continuously for "+str(desired_total_seconds/60)+" minutes"+".")
    print(settings_howto_msg)
    print("start_datetime: "+str(datetime.datetime.now()))
    try:
        print("#nominal_device_reading: "+str(tds[0].get_temperature(format=desired_format)))
    except:
        print("#Could not finish reading temperature from the device.")
        exit(3)
    print("#Please wait...")
    while (True):
        try:
            this_temp = tds[0].get_temperature(format=desired_format)
        except:
            print("#Could not finish reading temperature from the device." +
                  "#  The device seems to be disconnected.")
            print("exit_datetime: "+str(datetime.datetime.now()))
            print("exit_bake_seconds: "+str(current_bake.total_seconds))
            print("#exit_bake_minutes: "+str(current_bake.total_seconds/60))
            exit(4)
        current_span_temperatures_count += 1
        current_span_temperatures_total_temperature += this_temp
        current_temperatures.append(this_temp)
        if current_span_temperatures_count >= interval_seconds:
            this_avg = current_span_temperatures_total_temperature / current_span_temperatures_count
            this_min = min(current_temperatures)
            good_value = is_criteria_met(current_temperatures)
            del current_temperatures[:]
            met_msg = "("+opposite_operator[desired_comparison]+" "+str(desired_degrees)+") "
            #if (this_min >= desired_degrees):
            if good_value is not None:
                current_bake.temperatures.append(good_value)
                current_bake.total_seconds += current_span_temperatures_count
                met_msg = "("+desired_comparison+" "+str(desired_degrees)+") "
                if (current_bake.total_seconds>=desired_total_seconds):
                    current_bake.warmup_seconds = warmup_seconds
                    complete_bakes.append(current_bake)
                    current_bake = TSBake()
            else:
                if len(current_bake.temperatures) > 0:
                    if (current_bake.total_seconds<desired_total_seconds):
                        current_bake.warmup_seconds = warmup_seconds
                        incomplete_bakes.append(current_bake)
                        current_bake = TSBake()
                    else:
                        print("#Logic error detected (this should never happen): program did not end when "+process_term.lower()+" was successful (appending "+process_term.lower()+" to complete_"+process_term.lower()+"s anyway).")
                        current_bake.warmup_seconds = warmup_seconds
                        print("#current_pre"+process_term.lower()+"_minutes: "+str(current_bake.warmup_seconds/60))
                        complete_bakes.append(current_bake)
                        current_bake = TSBake()
            sustained_msg = ""
            if current_bake is not None and current_bake.total_seconds>0:
                #sustained_msg = "  # sustained:"+str(current_bake.total_seconds/60)+"m"
                sustained_msg = "  # remaining:"+str((desired_total_seconds-current_bake.total_seconds)/60)+"m"
            else:
                sustained_msg = "  # pre"+process_term.lower()+"_mins:"+str(warmup_seconds/60)
            print("#"+met_msg+"Last "+str(current_span_temperatures_count)+" second(s) avg:"+str(this_avg)+"; min:"+str(this_min)+sustained_msg)
            current_span_temperatures_count = 0
            current_span_temperatures_total_temperature = 0
            if (len(complete_bakes)>0):
                print("#"+process_term+" is finished: ")
                break
        time.sleep(1)
        warmup_seconds += 1

    print("incomplete_"+process_term.lower()+"s:")
    for bake in incomplete_bakes:
        print("  - minimum_temperatures: "+str(bake.temperatures))
        print("    pre"+process_term.lower()+"_minutes: "+str(bake.warmup_seconds/60))
        print("    "+process_term.lower()+"_minutes: "+str(bake.total_seconds/60))
    print("complete_"+process_term.lower()+"s:")
    for bake in complete_bakes:
        print("  - minimum_temperatures: "+str(bake.temperatures))
        print("    pre"+process_term.lower()+"_time_minutes: "+str(bake.warmup_seconds/60))
        print("    "+process_term.lower()+"_minutes: "+str(bake.total_seconds/60))
    print("incomplete_"+process_term.lower()+"s_count: "+str(len(incomplete_bakes)))
    print("complete_"+process_term.lower()+"s_count: "+str(len(complete_bakes)))
    print("end_datetime: "+str(datetime.datetime.now()))
    print("")

else:
    print("No TEMPer device found.")
