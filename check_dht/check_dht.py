#!/usr/bin/python2
#
# Simple nagios plugin to check temperature and humidity
# with a DHT22 one wire bus sensor or similar.
# Basically it only calls the Adafruit DHT driver and reads
# out the values.
# You can get the Adafruit DHT module at GitHub:
# https://github.com/adafruit/Adafruit_Python_DHT
#
# TODO: Use the nagios threshold syntax to make full use
# of the warning and critical thresholds.

import re
import subprocess
import time
import sys
import argparse
import Adafruit_DHT


def main():
    parser = argparse.ArgumentParser(description='Nagios plugin to check DHT sensors using Adafruit DHT driver')
    parser.add_argument('-s', '--sensor', required=False, help='Sensor to use (supported sensors: 11, 22, 2302)', default='22')
    parser.add_argument('-p', '--pin', required=False, help='GPIO pin number (example: -p 4)', default='4')
    parser.add_argument('-w', '--warning', required=False, help='warning threshold for temperature and humidity (example: -w 25,80)', default='25,80')
    parser.add_argument('-c', '--critical', required=False, help='warning threshold for temperature and humidity (example: -c 30,85)', default='30,85')
    args = parser.parse_args()

    sensor = args.sensor
    pin = args.pin
    warningTemp = args.warning.split(',')[0]
    warningHum = args.warning.split(',')[1]
    criticalTemp = args.critical.split(',')[0]
    criticalHum = args.critical.split(',')[1]

    sensor_args = { '11': Adafruit_DHT.DHT11,
            '22': Adafruit_DHT.DHT22,
            '2302': Adafruit_DHT.AM2302 }

    if sensor not in sensor_args:
        exitCheck(3, 'please select valid sensor (11, 22 or 2302)')
    else:
        sensor = sensor_args[sensor]

    hum, temp = Adafruit_DHT.read_retry(sensor, pin)
    if not re.match("\d+\.\d+", str(temp)):
        exitCheck(3, 'could not read temperature and humidity values')
    hum = float(round(hum,1))
    temp = float(round(temp,1))
    status = 0

    msg = "Temperature: %s Humidity: %s | temp=%s;%s;%s hum=%s;%s;%s" % (temp, hum, temp, warningTemp, criticalTemp, hum, warningHum, criticalHum)
    # process thresholds
    if re.match('\d+:\d+', warningTemp):
        warningTempLow, warningTempHigh = warningTemp.split(':')
        if temp < float(warningTempLow) or temp > float(warningTempHigh):
            status = 1
    elif temp > warningTemp:
            status = 1
    if re.match('\d+:\d+', warningHum):
        warningHumLow, warningHumHigh = warningHum.split(':')
        if hum < float(warningHumLow) or hum > float(warningHumHigh):
            status = 1
    elif hum > warningHum:
            status = 1
    if re.match('\d+:\d+', criticalTemp):
        criticalTempLow, criticalTempHigh = criticalTemp.split(':')
        if temp < float(criticalTempLow) or temp > float(criticalTempHigh):
            status = 2
    elif temp > criticalTemp:
            status = 2
    if re.match('\d+:\d+', criticalHum):
        criticalHumLow, criticalHumHigh = criticalHum.split(':')
        if hum < float(criticalHumLow) or hum > float(criticalHumHigh):
            status = 2
    elif hum > criticalHum:
            status = 2

    exitCheck(status, msg)


def exitCheck(status, msg=''):
    if status == 0:
        msg = 'OK - ' + msg
    elif status == 1:
        msg = 'WARNING - ' + msg
    elif status == 2:
        msg = 'CRITICAL - ' + msg
    elif status == 3:
        msg = 'UNKNOWN - ' + msg
    print msg
    sys.exit(status)


if __name__ == '__main__':
    sys.exit(main())
