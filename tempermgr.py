#!/usr/bin/env python

from __future__ import print_function
import sys
if sys.version_info.major >= 3:
    pass
else:
    input = raw_input


install_msg = '''
You do not have ccwienk/temper installed (not to be confused with the HTML templating engine named temper on pypi).
Please run the following commands in command line.
- If you are in Windows first run:
  cd C:\Python*
  or whatever is your Python directory.
- If you are using a Linux-like environment first run:
  sudo su -
  # you don't really need to sudo nor run as root (the program will show a message on how to add a udev rule if there is a PermissionError)
  # you don't really need to use --user if you use a virtualenv, the preferred install method
  # If are using a virtualenv such as creating using the
  # get_temp.sh script, there is no need to run any of these
  # install commands. Instead, run this script using
  #   ~/.virtualenvs/temper/bin/python
  # OR activate the virtualenv before running via:
  #   source ~/.virtualenvs/temper/bin/activate
  #   # and leave out "--user" from the following commands in that case

python -m pip install --user --upgrade pip
python -m pip install --user --upgrade pip wheel
python -m pip install --user --upgrade https://github.com/ccwienk/temper/archive/master.zip
'''
try_temperusb = False
_enable_temperusb = False
if try_temperusb:
    try:
        from temperusb import TemperDevice, TemperHandler
    except ImportError as ex:
        sys.stderr.write(str(ex)+"\n")
        sys.stderr.write(install_msg+"\n")
        sys.stderr.flush()
        _enable_temperusb = False


try:
    from temper import Temper
except ImportError as ex:
    sys.stderr.write(str(ex)+"\n")
    sys.stderr.write(install_msg+"\n")
    sys.stderr.flush()

no_dev_msg = '''
No TEMPer device found.
You must use a device supported by temper.
'''


opposite_operator = dict()
opposite_operator["<"] = ">="
opposite_operator["<="] = ">"
opposite_operator[">"] = "<="
opposite_operator[">="] = "<"

def f_to_c(f):
    return (f - 32) / 1.8


def c_to_f(c):
    return (c * 1.8) + 32


import getpass
user = getpass.getuser()
tryGroup = 'driverdev'

def permission_help():
    print("You must run with sudo, root, or add a udev rule via:")
    print()
    print("sudo groupadd {}".format(tryGroup))
    print('echo \'KERNEL=="hidraw*", SUBSYSTEM=="hidraw", MODE="0664",'
          ' GROUP="{}"\' | sudo tee /etc/udev/rules.d/'
          '99-hidraw-permissions.rules'.format(tryGroup))
    print('sudo usermod -a -G {} {}'.format(tryGroup, user))
    print('sudo udevadm control --reload-rules')
    print()
    print('# Then log out and back in if you\'re {}.'.format(user))


class TSBake:
    def __init__(self):
        self.temperatures = list()
        self.time = 0
        # ^ total_seconds
        self.warmTime = None


class TSSpan:
    '''
    An instance of this class holds the cumulative data for one given
    timespan based on the interval setting in seconds.
    '''

    def __init__(self):
        self.count = 0
        # ^ current_span_temperatures_count
        self.total = 0
        # ^ current_span_temperatures_total_temperature
        self.values = []
        # ^ current_temperatures


class TemperDeviceMgr:

    def __init__(self, tempermgr):
        self.tempermgr = tempermgr
        if tempermgr is None:
            raise RuntimeError("The TemperDeviceMgr class requires a"
                               " TemperMgr but the argument was None.")
        if _enable_temperusb:
            self.th = None
            try:
                self.th = TemperHandler()
            except:
                print("A TEMPerV1 compatible device is not plugged in,"
                      " or you have no permission to the usb device."
                      " Try running this script with sudo (sudo python"
                      " TemperatureSanitizer.py) or search online for"
                      " linux usb permissions.")
                exit(2)
            self.tds = self.th.get_devices()
            if len(self.tds) < 1:
                raise RuntimeError(no_dev_msg)
        self.tmpr = Temper()


    def getTemp(self, deviceIndex=0):
        '''
        Get the current temperature of the given device.

        raises:
        PermissionError (see the permission_help function)
        ValueError (bad settings['scale'])
        '''
        if _enable_temperusb:
            return self.tds[deviceIndex].get_temperature(
                format=self.tempermgr.get('scale')
            )
        devices = self.tmpr.read()
        if len(devices) < 1:
            raise RuntimeError("No TEMPer USB devices were detected.")
        c = devices[0]['internal temperature']
        if self.tempermgr.isF():
            return c_to_f(c)
        elif self.tempermgr.isC():
            return c
        else:
            scale = self.tempermgr.get('scale')
            raise ValueError("The scale {} is unknown.".format(scale))


class TemperMgr:

    def __init__(self, settings=None):
        self.defaults = {}
        self.settings = {}
        self.settings["target"] = 120
        # ^ desired_degrees
        self.settings["scale"] = "fahrenheit"
        # ^ desired_format
        self.settings["interval"] = 60
        # ^ interval_seconds
        self.settings["minTime"] = 120 * 60
        # ^ desired_total_seconds
        self.settings["compareOp"] = ">="
        # ^ desired_comparison
        self.settings['useStat'] = "average"
        # ^ desired_collate_method
        for k,v in self.defaults.items():
            self.settings[k] = v
        if settings is not None:
            for k,v in settings.items():
                self.settings[k] = settings[k]
        self._reinit()

    def _reinit(self):
        self.devicemgr = TemperDeviceMgr(self)
        self.process_term = "Bake"
        if self.settings["compareOp"] in ["<=","<"]:
            self.process_term = "Chill"
            if self.settings['useStat'] in ["max", "maximum"]:
                print("# WARNING: using min or average is recommended\n"
                      "# for chill,\n" +
                      "#   but you selected "
                      + self.settings['useStat'])

        self.complete_bakes = []
        self.incomplete_bakes = []

        self.bake = TSBake()
        # ^ current_bake
        self.warmTime = 0
        # ^ warmup_seconds
        self.span = TSSpan()

    def get(self, name):
        '''
        Get the value of a setting.

        Sequential arguments:
        name -- the name of the setting variable
        '''
        return self.settings.get(name)

    def isF(self):
        scale = self.get('scale')
        if scale.lower() == "fahrenheit":
            return True
        elif scale.lower() == "f":
            return True
        return False

    def isC(self):
        scale = self.get('scale')
        if scale.lower() == "celcius":
            return True
        elif scale.lower() == "c":
            return True
        return False

    def getTemp(self, deviceIndex=0):
        '''
        Get the temperature of the given device.

        raises:
        PermissionError (see the permission_help function)
        ValueError (if settings['scale'] is bad)
        '''
        return self.devicemgr.getTemp(deviceIndex)
        # ^ uses device 0 by default

    def iterate(self, passed, callback=print):
        '''
        Read the temperature and accumulate data into timespans then
        into bake(s).

        This is not a real iterator nor generator.
        Just run it every passed second(s) until it raises
        StopIteration.

        Sequential arguments:
        passed -- This must be the number of seconds that passed since
                  the previous call or no call to iterate. It should
                  usually be the same for every call in the session,
                  even the first call, since it represents the
                  theoretical "slice" of time during which a temperature
                  was present (inaccuracies with that practice are
                  mitigated using an interval setting greater than
                  passed).

        Raises:
        PermissionError (See the permission_help function)
        ValueError (if settings['scale'] is bad)
        StopIteration (if the bake is complete)
        '''
        # try:
        this_temp = self.getTemp()
        '''
        except:
            callback("#Couldn't finish reading temperature." +
                     "#  The device seems to be disconnected.")
            callback("exit_datetime: "+str(datetime.datetime.now()))
            callback("exit_bake_seconds: "+str(self.bake.time))
            callback("#exit_bake_minutes: "+str(self.bake.time/60))
            raise RuntimeError("The device is not accessible.")
        '''
        self.span.count += 1
        self.span.total += this_temp
        self.span.values.append(this_temp)
        if self.span.count >= self.get("interval"):
            this_avg = self.span.total / self.span.count
            this_min = min(self.span.values)
            good_value = self.is_criteria_met(self.span.values)
            del self.span.values[:]
            met_msg = ("("
                       + opposite_operator[self.settings["compareOp"]]
                       + " " + str(self.settings["target"]) + ") ")
            # if (this_min >= self.settings["target"]):
            if good_value is not None:
                self.bake.temperatures.append(good_value)
                self.bake.time += self.span.count
                met_msg = ("(" + self.settings["compareOp"] + " "
                           + str(self.settings["target"]) + ") ")
                if (self.bake.time >= self.settings["minTime"]):
                    self.bake.warmTime = self.warmTime
                    self.complete_bakes.append(self.bake)
                    self.bake = TSBake()
            else:
                if len(self.bake.temperatures) > 0:
                    if (self.bake.time < self.settings["minTime"]):
                        self.bake.warmTime = self.warmTime
                        self.incomplete_bakes.append(self.bake)
                        self.bake = TSBake()
                    else:
                        message = (
                            "#Logic error detected (this should never"
                            " happen): program did not end when "
                            + self.process_term.lower()
                            + " was successful (appending "
                            + self.process_term.lower()
                            + " to complete_"
                            + self.process_term.lower() + "s anyway)."
                        )
                        self.bake.warmTime = self.warmTime
                        print("#current_pre{}_minutes: {}"
                              "".format(self.process_term.lower(),
                                        self.bake.warmTime/60))
                        self.complete_bakes.append(self.bake)
                        self.bake = TSBake()
            sustained_msg = ""
            if (self.bake is not None) and (self.bake.time > 0):
                # sustained_msg = (
                # "  # sustained:{}m".format(self.bake.time/60)
                # )
                sustained_msg = "  # remaining:{}m".format(
                    (self.settings["minTime"]-self.bake.time)/60
                )
            else:
                sustained_msg = ("  # pre{}_mins:"
                                 "".format(self.process_term.lower(),
                                           self.warmTime/60))
            print("#" + met_msg + "Last "
                  + str(self.span.count)
                  + " second(s) avg:" + str(this_avg) + "; min:"
                  + str(this_min) + sustained_msg)
            self.span.count = 0
            self.span.total = 0
            if len(self.complete_bakes) > 0:
                print("#"+self.process_term+" is finished: ")
                raise StopIteration
        self.warmTime += passed

    def is_criteria_met(self, temperatures):
        # formerly is_criteria_met
        result = None
        operand = None
        if self.settings['useStat'] in ["min","minimum"]:
            operand = min(temperatures)
        elif self.settings['useStat'] in ["max","maximum"]:
            operand = max(temperatures)
        elif self.settings['useStat'] in ["avg","average"]:
            operand = sum(temperatures) / float(len(temperatures))
        else:
            print("# settings['useStat'] must be: \n" +
                  "#   min, max, or average")
            exit(5)
        met_enable = False
        if self.settings["compareOp"] == ">=":
            met_enable = (operand >= self.settings["target"])
        elif self.settings["compareOp"] == ">":
            met_enable = (operand > self.settings["target"])
        elif self.settings["compareOp"] == "<=":
            met_enable = (operand <= self.settings["target"])
        elif self.settings["compareOp"] == "<":
            met_enable = (operand < self.settings["target"])
        else:
            print("# Unknown comparison was selected. Please use: \n" +
                  "#   <, <=, >, or >=")
            exit(6)
        if met_enable:
            result = operand
        return result
