# TemperatureSanitizer
TemperatureSanitizer detects when a minimum temperature is sustained for a minimum time. This program uses temperusb aka temper, and default settings are for killing bedbugs (set to 120mins though 90 is considered minimum, and 120 degrees fahrenheit though 118 is considered minimum).

In addition to the GPL 3.0 license, the following disclaimer applies: THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## Requirements
* A TEMPerV1 compatible USB thermometer (can be ordered online)
* temperusb library for python (if your python does not have temperusb is not installed yet, the program will detect that problem and instruct you how to correct that). Installing temperusb requires the temperusb whl file or an internet connection in order to follow those instructions displayed by this program.

## Planned Features
* support TEMPered
  * Where `/dev/hidraw4` is the correct device (could be any number), run `hid-query /dev/hidraw4 0x01 0x80 0x33 0x01 0x00 0x00 0x00 0x00`

  * an example of parsing the output is at <https://github.com/padelt/temper-python/issues/84#issuecomment-393930865>
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
fi
```

## Known Issues
* Does not support TEMPer with USB ID 413d:2107 (try lsusb to see your ID while device is plugged in). This project should use https://github.com/edorfaus/TEMPered instead of temperusb (which has not responded to this issue on GitHub)

## Usage
* Make sure you place the temperature sensor in a "cold spot," such as (if you are using this program to monitor a bedbug oven) inside a book in the middle of your load.
* Change the following settings by editing the py file:
```python
desired_degrees = 120
desired_format = "fahrenheit"
interval_seconds = 60
desired_total_seconds = 120 * 60
```
    * and, if you want to chill instead of bake, you can edit the following settings also in the py file:
    ```python
    desired_comparison = ">="
    desired_collate_method = "average"
    ```
    * desired_comparison can be ">=", ">", "<=", or "<"
    * desired_collate_method can be minimum (or min), maximum (or max), or average (or avg) -- for example, for a chill (using < or <=), min or average would be appropriate comparisons to ensure that a temperature reading never was above the desired temperature; but for baking (using >= or >), min or average would be recommended, where min would ensure a temperature reading didn't dip below desired temperature.

* How the settings are used by the program:
    * desired_format can be "fahrenheit" or "celcius".
    * The interval may need to be at least a few seconds for accuracy, though an interval of 1 can be used if you don't mind having all that data, and your sensor is accurate enough for that type of use (trusting a single reading as part of your raw data).
    * The temperature is always checked every second. This is not configurable, but only the minimum and avarage are displayed from each interval, which is a group of these secondly readings.
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
* (2017-04-09) Display remaining time while temperature is >= minimum
* (2017-04-09) Display system time when finished
* (2017-04-08) Renamed variables for clarity, and added a region called User Settings to distinguish those variables from the rest of the code.


## Known Issues
(None)

## Developer Notes
* The settings are hard-coded, in the User Settings region of the py file.
* When a span is complete, the span is added to the bake only if the minimum temperature of the span meets the desired temperature.
