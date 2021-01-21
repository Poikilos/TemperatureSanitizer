# TemperatureSanitizer
TemperatureSanitizer detects when a minimum temperature is sustained for a minimum time. The default settings are for killing bedbugs:
- 120 minutes (though 90 minutes is considered minimum)
- 120 degrees fahrenheit (though 118 is considered minimum).

The settings of this software also allow for a "chill" rather than a "bake", so it is suitable for various purposes. A real timespan rather than a delay is necessary for a level of accuracy necessary for science (this could be accomplished by modifying TemperatureSanitizer.py). Using a delay rather than a calculated timespan between reads errs on the side of overkill (only by milliseconds, if that, though), so the delay is reliable for scenarios where fractions of a second more than the allotted time are acceptable. Also, the counting doesn't start until the temperature is reached, so the bake may approach an extra minute long if the previous interval of 60 seconds (or whatever amount you set for settings['interval']) had reached the temperature at some point but not enough to meet the stat requirement (settings['useStat'] can be the min, max, or avg of the interval).

Bedbug ovens are available from ThermalStrike (I use ThermalStrike Ranger for a low-cost option) or [ZappBug on Amazon](https://www.amazon.com/s?k=ZappBug).

For sustaining a minimum temperature, try to place the temperature sensor in the coolest spot (such as the innermost part of the most insulated part of the load).

Beware of bedbug myths. They don't "die instantly" in the dryer. People often rid themselves of fleas and think they killed bedbugs easily, but bedbugs don't die easily. See the related NIH study under "Reference Temperatures" for a reliable approach.


## Reference Temperatures
According to [Temperature and Time Requirements for Controlling Bed Bugs (Cimex lectularius) under Commercial Heat Treatment Conditions ](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4553552/) by Stephen A. Kells* and Michael J. Goblirsch, bedbug eggs can survive 71.5 min at 48 °C. Therefore, go longer or higher than that to be sure. Note that your temperature sensor may not be in the coolest spot (attempt to place it in a cool spot). The lethal temperature "for eggs was 54.8 °C" in the study, while the sub-lethal temperatures took longer. Reaching the acute temperature may be impossible in some cases of a large bug oven or house heat treatment, and the acute temperature is more likely to damage your property or bedbug oven. Therefore, the lower temperature and longer times are the defaults for this program, as listed at the beginning of this document.

Conversions table for reference temperatures:
- 113° F = 45° C
- 118.4° F = 48° C
- 120° F = 48.8889° C
- 130.64 F = 54.8 C


## Requirements
The scripts will detect missing dependencies and instruct you how to correct that
- A TEMPer compatible USB thermometer (can be ordered online)
- [github.com/ccwienk/temper](https://github.com/ccwienk/temper) or another fork of urwen/temper (NOT the pypi package which is also named temper but is an HTML templating engine)
  - get_temp.sh installs it into a virtualenv automatically (run.sh calls it as well, so you can use run.sh as a more reliable way of calling TemperatureSanitizer.py)


## Usage
* Make sure you place the temperature sensor in a "cold spot," such as (if you are using this program to monitor a bedbug oven) inside a book in the middle of your load.
* Change the following settings by editing TemperatureSanitizer or utilizing tempermgr as a library similarly to how TemperatureSanitizer.py does. A settings dictionary passed to the TemperMgr constructor can include the following settings (the defaults are below):
  ```python
settings = {}
settings['target'] = 120
settings['scale'] = "fahrenheit"
settings['interval'] = 60  # the interval in seconds (get one average or other specified stat per interval)
settings['minTime'] = 120 * 60  # the total desired time at the temperature
```
  * and, if you want to chill instead of bake, you can edit the following settings:
      ```python
    settings['compareOp'] = ">="
    settings['useStat'] = "average"
```
  * `settings['compareOp']` can be ">=", ">", "<=", or "<"
  * `settings['useStat']` can be minimum (or min), maximum (or max), or average (or avg) -- for example, for a chill (using < or <=), min or average would be appropriate comparisons to ensure that a temperature reading never was above the desired temperature; but for baking (using >= or >), min or average would be recommended, where min would ensure a temperature reading didn't dip below desired temperature.

* How the settings are used by the program:
  * scale can be "fahrenheit" or "celcius".
  * The interval may need to be at least a few seconds for accuracy, though an interval of 1 can be used if you don't mind having all that data, and your sensor is accurate enough for that type of use (trusting a single reading as part of your raw data).
  * The temperature is always checked every second. This is not configurable, but only the minimum and avarage are displayed from each interval, which is a group of these secondly readings.
  * The seconds will start counting when the minimum temperature of the interval is at least at the settings['target'] temperature. If the total number of seconds of bake time is reached (when there was a consecutive set of spans where the minimum never was below settings['target'] temperature), the program will end and show a summary (including a list of temperatures, each of which is the minimum temperature of each consecutive interval that had the desired temperature as its minimum). Otherwise, the program will continue collecting data indefinitely.
* Run:
```bash
# cd to the directory where you saved the py file, then:
sudo python TemperatureSanitizer
# Or, run without sudo if you have changed the permissions of your USB device.
# NOTE: sometimes that setting is forgotten when the device is unplugged and
# reinserted, even if same port is used.
```


## Known Issues
See [github.com/poikilos/TemperatureSanitizer/issues](https://github.com/poikilos/TemperatureSanitizer/issues).

When reporting issues, provide the USB id of your device, such as via
`lsusb` on Linux (run it before and after inserting the device to see
what appears, as it may not have any name by the id string).

## Developer Notes
* The settings are hard-coded, in the User Settings region of the py file.
* When a span is complete, the span is added to the bake only if the minimum temperature of the span meets the desired temperature.

### Deprecated
- temperusb: The temperusb library (see `try_temperusb` in tempermgr.py) only supports TEMPerV1. Installing temperusb requires the temperusb whl file or an internet connection in order to follow those instructions displayed by this program.

### Discarded plans
#### TEMPered

#### Include or compile hid-query
Where `/dev/hidraw4` is the correct device (could be any number--usually last one listed via `ls /dev | grep hidraw`),
run `sudo hid-query /dev/hidraw1 0x01 0x80 0x33 0x01 0x00 0x00 0x00 0x00`
the response is 8 bytes such as:
`80 80 0a fc  4e 20 00 00`
where 0a fc is an integer (2825 in this case). Divide that by 100 to get the temperature.

An example of parsing the output is at
<https://github.com/padelt/temper-python/issues/84#issuecomment-393930865>
(possibly auto-install TEMPered such as with script below)
```bash
if [ ! `which hid-query` ]; then
  cd $HOME
  if [ ! -d Downloads ]; then mkdir Downloads; fi
  cd Downloads
  if [ ! -d TEMPered ]; then
    git clone https://github.com/edorfaus/TEMPered.git
    cd TEMPered
  else
    cd TEMPered
    git pull
  fi
  if [ ! -d build ]; then mkdir build; fi
  cd build
  cmake ..
  sudo make install
  if [ ! -d /usr/local/lib ]; then mkdir -p /usr/local/lib; fi
  sudo cp libtempered/libtempered.so.0 /usr/local/lib/
  sudo cp libtempered-util/libtempered-util.so.0 /usr/local/lib/
  sudo ln -s /usr/local/lib/libtempered.so.0 /usr/local/lib/libtempered.so
  sudo ln -s /usr/local/lib/libtempered-util.so.0 /usr/local/lib/libtempered-util.so
fi
```

Find hid like:
```bash
  #LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib tempered
  # previous line doesn't work for some reason so:
  hid-query --enum
  # lists 2 for some reason:
  # /dev/hidraw0 : 413d:2107 interface 0 : (null) (null)
  # /dev/hidraw1 : 413d:2107 interface 1 : (null) (null)
```

A script such as readTEMPer-driverless-withdate.sh (by jbeale1 from link above) could be made like:
```bash
#!/bin/bash
OUTLINE=`sudo ./hid-query /dev/hidraw3 0x01 0x80 0x33 0x01 0x00 0x00 0x00 0x00|grep -A1 ^Response|tail -1`
OUTNUM=`echo $OUTLINE|sed -e 's/^[^0-9a-f]*[0-9a-f][0-9a-f] [0-9a-f][0-9a-f] \([0-9a-f][0-9a-f]\) \([0-9a-f][0-9a-f]\) .*$/0x\1\2/'`
HEX4=${OUTNUM:2:4}
DVAL=$(( 16#$HEX4 ))
bc <<< "scale=2; $DVAL/100"
```

The script above would be used like:
```bash
while [ true ]; do
  temp=`./readTEMPer-driverless-withdate.sh`
  echo $(date +"%F %T") " , " $temp
  sleep 14
done
```
