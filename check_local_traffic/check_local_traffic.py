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
	# if last value seems incorrect, can happen after reboot
	if	trafficDataOld['rx_bytes'] >= trafficDataNew['rx_bytes'] or \
		trafficDataOld['tx_bytes'] >= trafficDataNew['tx_bytes'] or \
		trafficDataOld['rx_bytes'] == 0 or \
		trafficDataOld['tx_bytes'] == 0:
		avgBytesRX = 0
		avgBytesTX = 0
		diffBytesRX = 0
		diffBytesTX = 0
	else:
		diffBytesRX = (trafficDataNew['rx_bytes'] - int(trafficDataOld['rx_bytes'])) 
		diffBytesTX = (trafficDataNew['tx_bytes'] - int(trafficDataOld['tx_bytes'])) 
		avgBytesRX = int( diffBytesRX / deltaTime)
		avgBytesTX = int( diffBytesTX / deltaTime)
	
	trafficDataOutput = dict()	
	trafficDataOutput['avgBytesRX'] = avgBytesRX
	trafficDataOutput['avgBytesTX'] = avgBytesTX
	trafficData.setData()
	return trafficDataOutput



def doCheck(device):
	trafficData = processData(device)

	if trafficData is not False:
		textOutput = str("OK - device " + device + " "  
				" avgBytesRX " + str(trafficData['avgBytesRX']) +
				" avgBytesTX " + str(trafficData['avgBytesTX']) +
				" |" +  
				" avgBytesRX=" + str(trafficData['avgBytesRX']) +
				" avgBytesTX=" + str(trafficData['avgBytesTX'])	)
		returnCode = 0
	else:
		textOutput = 'UNKNOWN - device ' + device + ' not found'
		returnCode = 3

	print(textOutput)
	return returnCode



if __name__ == '__main__':
	sys.exit(main())
