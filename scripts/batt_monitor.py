#!/usr/bin/env python
# coding: latin-1
import rospy
from std_msgs.msg import Header
from std_msgs.msg import Float32
from batt_monitor_publisher.msg import BatteryMonitor  
import Adafruit_ADS1x15

# Configuration
ADS_GAIN = 2
ADS_HALF_RES = 2048
ADS_FULL_VOLTAGE = 4.096
VOLTAGE_DIVIDER_RATIO = 10.1
CURRENT_SENSOR_SCALE = 10  # Replace with actual scale for current sensor
MOVING_AVERAGE_SIZE = 10  # Number of samples for moving average

def moving_average(new_reading, readings_list):
    readings_list.append(new_reading)
    if len(readings_list) > MOVING_AVERAGE_SIZE:
        readings_list.pop(0)
    return sum(readings_list) / len(readings_list)

def scale_adc_value(adc_value, original_min, original_max, new_min, new_max, scale):
    return (((adc_value - original_min) / float(original_max - original_min)) * (new_max - new_min) + new_min) * scale

def read_voltage(adc):
    adc_value = max(0, adc.read_adc(0, gain=ADS_GAIN))
    scaled_voltage = scale_adc_value(adc_value, 0, ADS_HALF_RES, 0, ADS_FULL_VOLTAGE / ADS_GAIN, VOLTAGE_DIVIDER_RATIO)
    return scaled_voltage

def read_current(adc):
    adc_value = max(0, adc.read_adc(1, gain=ADS_GAIN))
    scaled_current = scale_adc_value(adc_value, 0, ADS_HALF_RES, 0, ADS_FULL_VOLTAGE / ADS_GAIN, CURRENT_SENSOR_SCALE)
    return scaled_current

def adc_publisher():
    rospy.init_node('batt_monitor_pub', anonymous=True)
    battery_monitor_pub = rospy.Publisher('batt_monitor', BatteryMonitor, queue_size=10)

    rate = rospy.Rate(10)  # 10hz

    adc = Adafruit_ADS1x15.ADS1015()
    voltage_readings = []
    current_readings = []

    while not rospy.is_shutdown():
        voltage = read_voltage(adc)
        current = read_current(adc)

        average_voltage = moving_average(voltage, voltage_readings)
        average_current = moving_average(current, current_readings)

        battery_monitor_msg = BatteryMonitor()
        battery_monitor_msg.header.stamp = rospy.Time.now()
        battery_monitor_msg.voltage = round(average_voltage, 2)
        battery_monitor_msg.current = round(average_current, 2)

        battery_monitor_pub.publish(battery_monitor_msg)
        
        rate.sleep()

if __name__ == '__main__':
    try:
        adc_publisher()
    except rospy.ROSInterruptException:
        pass
