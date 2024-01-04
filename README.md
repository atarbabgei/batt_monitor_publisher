## Overview
The `batt_monitor_publisher` package is a ROS1 package for monitoring and publishing battery data, specifically voltage and current readings. It uses an Adafruit ADS1x15 ADC to read the voltage and current, processes these readings, and publishes them as ROS messages.

## Dependencies
- ROS Melodic (or the ROS version you are using)
- Adafruit_ADS1x15 Python library
- std_msgs ROS package
- Python 2.7

## Compatibility
- Tested in ROS Melodic
