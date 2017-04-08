# TemperatureSanitizer
TemperatureSanitizer detects when a minimum temperature is sustained for a minimum time. This program uses temperusb aka temper, and default settings are for killing bedbugs (set to 120mins though 90 is considered minimum, and 120 degrees fahrenheit though 118 is considered minimum).

## Requirements:
* A TEMPerV1 compatible USB thermometer (can be found online)
* temperusb library for python (if your python does not have temperusb is not installed yet, the program will detect that problem and instruct you how to correct that). Installing temperusb requires the temperusb whl file or an internet connection in order to follow those instructions displayed by this program.

## Usage
* Change the following settings by editing the py file:
```python
desired_degrees = 120
desired_format = "fahrenheit"
interval_seconds = 60
desired_total_seconds = 120 * 60
```
* How the settings are used by the program:
    * desired_format can be "fahrenheit" or "celcius".
    * The interval may need to be at least a few seconds for accuracy, though an interval of 1 can be used if you don't mind having all that data, and your sensor is accurate enough for that type of use (trusting a single reading as part of your raw data).
    * The seconds will start counting when the minimum temperature of the interval is at least desired_degrees. If the total number of seconds of bake time is reached (when there was a consecutive set of spans where the minimum never was below desired_degrees), the program will end and show a summary (including a list of temperatures, each of which is the minimum temperature of each consecutive interval that had the desired temperature as its minimum). Otherwise, the program will continue collecting data indefinitely.
* Run:
```bash
# cd to the directory where you saved the py file, then:
sudo python TemperatureSanitizer
# Or, run without sudo if you have changed the permissions of your USB device.
# NOTE: sometimes that setting is forgotten when the device is unplugged and
# reinserted, even if same port is used.
```


## Changes
* (2017-04-08) Ranamed variables for clarity, and added a region called User Settings to distinguish those variables from the rest of the code.

## Developer Notes
* The settings are hard-coded, in the User Settings region of the py file
* When a span is complete, the span is added to the bake only if the minimum temperature of the span meets the desired temperature.
