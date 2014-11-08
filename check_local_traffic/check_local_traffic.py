#!/usr/bin/env python
"""
    check_python.py - simple nagios plugin to check traffic on linux hosts
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


__author__ = "Finn Christiansen"
__copyright__ = "Copyright 2012-2013, Finn Christiansen"
__credits__ = ["Finn Christiansen"]
__license__ = "GPL"
__version__ = "3"
__maintainer__ = "Finn Christiansen"
__email__ = "kontakt@finnchristiansen.de"
__status__ = "Development"


import sys
import re
import os
import shelve
import time
import argparse
import math


class PluginData:
	def __init__(self, device):
		self.storePath = '/tmp/check_local_traffic_%s' % device
		self.statsPath = '/sys/class/net/%s/statistics/' % device
		self.values = ['collisions', 'multicast', 'rx_bytes', 'rx_compressed', 'rx_crc_errors', 'rx_dropped', 'rx_errors', 'rx_fifo_errors', 'rx_frame_errors', 'rx_length_errors', 'rx_missed_errors', 'rx_over_errors', 'rx_packets', 'tx_aborted_errors', 'tx_bytes', 'tx_carrier_errors', 'tx_compressed', 'tx_dropped', 'tx_errors', 'tx_fifo_errors', 'tx_heartbeat_errors', 'tx_packets', 'tx_window_errors']
		if not os.path.isfile(self.storePath):
			self.getData()
			self.setData()

	def initData(self):
		self.data = dict()
		for key in self.values:
			self.data[key] = int(open('%s%s' % (self.statsPath, key)).read())
		self.data['timeLastCheck'] = time.time() 
		
	def getData(self):
		self.data = dict()
		try:
			for key in self.values:
				self.data[key] = int(open('%s%s' % (self.statsPath, key)).read())
		except IOError as e:
			return False	
		self.data['timeLastCheck'] = time.time() 
		return self.data
	
	def setData(self):
		pluginStore = shelve.open(self.storePath)
		pluginStore['pluginData'] = self.data
		pluginStore.close()
		return True

	def getStoredData(self):
		pluginDataFile = shelve.open(self.storePath)
		pluginData = pluginDataFile['pluginData']
		pluginDataFile.close()
		return pluginData

def main():
	parser = argparse.ArgumentParser(description = 'Nagios plugin to check traffic usage')
	parser.add_argument('-d', '--device', required=True)
	args = parser.parse_args()
	if args.device is not None:
		returnCode = doCheck(args.device)
	else:
		returnCode = 3

	return returnCode


def processData(device):
	trafficData = PluginData(device)
	trafficDataOld = trafficData.getStoredData()
	trafficDataNew = trafficData.getData()
	if trafficDataNew is False:
		return False

	deltaTime = time.time() - trafficDataOld['timeLastCheck']
	trafficDataOutput = dict()

	# if last value seems incorrect... can happen after reboot
	if	trafficDataOld['rx_bytes'] > trafficDataNew['rx_bytes'] or \
		trafficDataOld['tx_bytes'] > trafficDataNew['tx_bytes'] or \
		trafficDataOld['rx_bytes'] == 0 or \
		trafficDataOld['tx_bytes'] == 0:
		for key in trafficDataNew:
			trafficDataOutput[key] = 0
	else:
		for key in trafficDataNew:
			trafficDataOutput[key] = (int(trafficDataNew[key]) - int(trafficDataOld[key])) / deltaTime

	trafficData.setData()
	return trafficDataOutput



def doCheck(device):
	trafficData = processData(device)

	if trafficData is not False:
		perfdataString  = "bits_in/s={0:.3f};".format(trafficData['rx_bytes']*8)
		perfdataString += " bits_out/s={0:.3f};".format(trafficData['tx_bytes']*8)
                textOutput = "OK - %s in: %s - out: %s | %s" % (device,
                        formatBits(trafficData['rx_bytes']),
                        formatBits(trafficData['tx_bytes']), perfdataString)
		returnCode = 0
	else:
		textOutput = 'UNKNOWN - device ' + device + ' not found'
		returnCode = 3

	print(textOutput)
	return returnCode

def formatBits(value):
    output = value * 8
    size_names = ["bit/s", "kbit/s", "Mbit/s", "Gbit/s"]
    i = 0
    while output > 1024:
        output = output / 1024
        i += 1
    return "{0:.3f};".format(output) + " " + size_names[i]


if __name__ == '__main__':
	sys.exit(main())
