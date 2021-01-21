# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).


## [git] - 2021-01-21
### Added
- support `-f` option for fahrenheit in get_temp.sh and read-loop.sh.

### Changed
- Move business logic and related variables including settings to a class.
- Move settings to a dict named `settings` and rename them as follows:
  - `desired_degrees` to `target`.
  - `desired_format` to `scale`.
  - `interval_seconds` to `interval`.
  - `desired_total_seconds` to `minTime`.
  - `desired_comparison` to `compareOp`.
  - `desired_collate_method` to `useStat`.
- Use ccwienk/temper in TemperatureSanitizer.py for improved compatibility.


## [git] - 2021-01-20
### Added
- Support more devices using ccwienk/temper, a fork of urwen/temper, but
  only in get_temp.sh (which read-loop.sh uses if hid-query isn't
  present)
  - Tested with 413d:2107 (applies to [Jepeak Temper High Accurate USB Thermometer Temperature Sensor Data Logger Record for PC Laptop](https://www.amazon.com/gp/product/B009YRP906/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1) and others)

### Changed
- Move changes to Changelog.


## [git] - 2017-04-09
### Changed
- Display remaining time while temperature is >= minimum
- Display system time when finished


## [git] - 2017-04-08
### Added
- Add a region called User Settings to distinguish those variables from
  the rest of the code.

### Changed
- Renamed variables for clarity

