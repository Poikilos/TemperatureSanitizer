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
    print("You have no permission to the usb device. Please run this python script with sudo or search online for linux usb permissions.")
    exit(2)
tds = th.get_devices()
this_count = 0
this_total = 0
desired_degrees = 120
desired_format = "fahrenheit"
desired_interval_seconds = 60
desired_total_seconds = 120 * 60

class TimeStretch:
    def __init__(self):
        self.temperatures = list()
        self.total_seconds = 0

good_stretches = list()
bad_stretches = list()

this_stretch = TimeStretch()
this_temperatures = list()
if (len(tds)>0):
    print("This program will show minimum temperature every "+str(desired_interval_seconds)+" second(s), whether that span met (>=) the desired minimum, and will tell you after the temperature has been the desired minimum of "+str(desired_degrees)+" "+desired_format+" for any continuous stretch of "+str(desired_total_seconds/60)+" minutes (which is "+str(desired_total_seconds)+" seconds)"+".")
    print("Please wait...")
    while (True):
        this_temp = tds[0].get_temperature(format=desired_format)
        this_count += 1
        this_total += this_temp
        this_temperatures.append(this_temp)
        if this_count >= desired_interval_seconds:
            this_avg = this_total / this_count
            this_min = min(this_temperatures)
            del this_temperatures[:]
            met_msg = "(< "+str(desired_degrees)+") "
            if (this_min >= desired_degrees):
                this_stretch.temperatures.append(this_min)
                this_stretch.total_seconds += this_count
                met_msg = "(>= "+str(desired_degrees)+") "
                if (this_stretch.total_seconds>=desired_total_seconds):
                    good_stretches.append(this_stretch)
                    this_stretch = TimeStretch()
            else:
                if len(this_stretch.temperatures) > 0:
                    if (this_stretch.total_seconds<desired_total_seconds):
                        bad_stretches.append(this_stretch)
                        this_stretch = TimeStretch()
                    else:
                        good_stretches.append(this_stretch)
                        this_stretch = TimeStretch()
                    
            print(met_msg+"Last "+str(this_count)+" second(s) average:"+str(this_avg)+"; minimum:"+str(this_min))
            this_count = 0
            this_total = 0
            if (len(good_stretches)>0):
                print("Baking is finished: ")
                break
        time.sleep(1)

    print("Complete bake(s):")
    for stretch in good_stretches:
        print("  - Temperatures: "+str(stretch.temperatures))
        print("    seconds: "+str(stretch.total_seconds))
    print()
    print("Incomplete bake(s):")
    for stretch in bad_stretches:
        print("  - Temperatures: "+str(stretch.temperatures))
        print("    seconds: "+str(stretch.total_seconds))

else:
    print("No TEMPer device found.")
