#!/usr/bin/env python
"""
    check_local_traffic.py - simple nagios plugin to check traffic on linux
    hosts
    Copyright (C) 2012 Finn Christiansen

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

This is a small nagios plugin used for checking or watching the traffic on
linux host by reading /sys/class/net/<device>/statistics/* and storing
information in a file to calculate the average and total traffic.
Currently it can be only used to get performance data, warning and critial
values will be added soon.

"""

import sys
import re
import os
import shelve
import time
import argparse
import math


storePath = '/tmp/check_local_traffic_%s'
statsPath = '/sys/class/net/%s/statistics/'


def getCurrentData(device):
    values = [
        'collisions', 'multicast', 'rx_bytes', 'rx_compressed',
        'rx_crc_errors', 'rx_dropped', 'rx_errors', 'rx_fifo_errors',
        'rx_frame_errors', 'rx_length_errors', 'rx_missed_errors',
        'rx_over_errors', 'rx_packets', 'tx_aborted_errors', 'tx_bytes',
        'tx_carrier_errors', 'tx_compressed', 'tx_dropped', 'tx_errors',
        'tx_fifo_errors', 'tx_heartbeat_errors', 'tx_packets',
        'tx_window_errors'
        ]

    data = dict()
    for key in values:
        data[key] = int(open('%s%s' % (statsPath % device, key)).read())
    data['timeLastCheck'] = time.time()

    if not os.path.isfile(storePath % device):
        data = getCurrentData(device)
        setData(device, data)
    data = dict()
    try:
        for key in values:
            data[key] = int(open('%s%s' % (statsPath % device, key)).read())
    except IOError as e:
        return False
    data['timeLastCheck'] = time.time()
    return data


def setData(device, data):
    pluginStore = shelve.open(storePath % device)
    pluginStore['pluginData'] = data
    pluginStore.close()
    return True


def getStoredData(device):
    try:
        pluginDataFile = shelve.open(storePath % device)
        pluginData = pluginDataFile['pluginData']
        pluginDataFile.close()
    except:
        pluginData = getCurrentData(device)
    return pluginData


def doCheck(device, warning, critical):
    if os.path.isdir(statsPath % device):
        trafficDataOld = getStoredData(device)
        trafficDataNew = getCurrentData(device)
        if trafficDataNew is False:
            return False

        deltaTime = time.time() - trafficDataOld['timeLastCheck']
        trafficData = dict()

        # if last value seems incorrect... can happen after reboot
        if (trafficDataOld['rx_bytes'] > trafficDataNew['rx_bytes'] or
                trafficDataOld['tx_bytes'] > trafficDataNew['tx_bytes'] or
                trafficDataOld['rx_bytes'] == 0 or
                trafficDataOld['tx_bytes'] == 0):
            for key in trafficDataNew:
                trafficData[key] = 0
        else:
            for key in trafficDataNew:
                trafficData[key] = (int(trafficDataNew[key]) -
                                    int(trafficDataOld[key])) / deltaTime

        setData(device, trafficDataNew)

        if trafficData is not False:
            bits_in = trafficData['rx_bytes']*8
            bits_out = trafficData['tx_bytes']*8

            if warning and critical:
                if bits_in < warning and bits_out < warning:
                    returnCode = 0
                    prefix = "OK"
                elif bits_in < critical and bits_out < critical:
                    returnCode = 1
                    prefix = "WARNING"
                else:
                    returnCode = 2
                    prefix = "CRITICAL"
                thresholds = "%s;%s;" % (warning, critical)
            else:
                returnCode = 0
                prefix = "OK"
                thresholds = ''

            perfdataString = "bits_in/s={0:.3f};%s".format(bits_in) % \
                thresholds
            perfdataString += " bits_out/s={0:.3f};%s".format(bits_out) % \
                thresholds
            textOutput = " - %s in: %s - out: %s | %s" % \
                (device, formatBits(bits_in), formatBits(bits_out),
                    perfdataString)

            textOutput = prefix + textOutput
        else:
            textOutput = 'UNKNOWN - device ' + device + ' not found'
            returnCode = 3
    else:
        textOutput = 'UNKNOWN - device ' + device + ' not found'
        returnCode = 3
    print(textOutput)
    return returnCode


def formatBits(value):
    output = value
    size_names = ["bit/s", "kbit/s", "Mbit/s", "Gbit/s"]
    i = 0
    while output > 1024:
        output = output / 1024
        i += 1
    return "{0:.3f};".format(output) + " " + size_names[i]


def deviceExists(device):
    exists = False
    if os.path.isfile(statsPath % device):
        exists = False
    return exists


def readThresholds(value):
    if re.match('\d+k', value):
        plain_value = int(value[0:-1]) * 1024
    elif re.match('\d+M', value):
        plain_value = int(value[0:-1]) * 1024*1024
    elif re.match('\d+G', value):
        plain_value = int(value[0:-1]) * 1024*1024*1024
    else:
        plain_value = value
    return plain_value


def main():
    parser = argparse.ArgumentParser(description='Nagios plugin to check \
            traffic usage')
    parser.add_argument('-d', '--device', required=True)
    thresholds = parser.add_argument_group('thresholds',
                                           'warning and critical thresholds \
                                            (k, M, G may be used)')
    thresholds.add_argument('-w', '--warning', default=False)
    thresholds.add_argument('-c', '--critical', default=False)

    args = parser.parse_args()
    if args.warning and args.critical:
        args.warning = readThresholds(args.warning)
        args.critical = readThresholds(args.critical)
    if args.device is not None:
        returnCode = doCheck(args.device, args.warning, args.critical)
    else:
        returnCode = 3

    return returnCode

if __name__ == '__main__':
    sys.exit(main())
