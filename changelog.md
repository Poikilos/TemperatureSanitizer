# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),


## [git] - 2021-01-20
### Added
- Support more devices using ccwienk/temper, a fork of urwen/temper, but
  only in get_temp.sh (which read-loop.sh uses if hid-query isn't
  present).
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

