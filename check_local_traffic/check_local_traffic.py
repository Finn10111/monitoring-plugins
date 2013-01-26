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
linux host by reading /proc/dev/net and storing information in a file
to calculate the average and total traffic. Currently it can be only used 
to get performance data, warning and critial values will be added soon.

"""


__author__ = "Finn Christiansen"
__copyright__ = "Copyright 2012, Finn Christiansen"
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


class Usage(Exception):
	def __init__(self, msg):
		self.msg = msg

 
def main():
	parser = argparse.ArgumentParser(description = 'Nagios check for traffic usage')
	parser.add_argument('-d', '--device', required=True)
	args = parser.parse_args()
	if args.device is not None:
		doCheck(args.device)
	else:
		return 2


def getDevData(device):
	infile = open('/proc/net/dev', 'r')
	devData = None	
	for line in infile:
		if re.match('.*' + device + ':.*', line):
			devData = re.sub('\:', ' ',  line)
	infile.close()
	if devData is not None:
		devData = re.sub('\s{2,}', ' ', devData.strip()).split(' ')
		devData.append(int(time.time()))
		return devData
	else:
		return False

	
def processData(device, devData):
	trafficDataPath = '/tmp/check_local_traffic_'+device
	if os.path.isfile(trafficDataPath):
		trafficDataFile = shelve.open(trafficDataPath)
		trafficData = trafficDataFile['trafficData']
		deltaTime = time.time() - trafficData['timeLastCheck']
		currBytesRX = int(devData[1])
		currBytesTX = int(devData[9])
		if	trafficData['lastBytesRX'] >= currBytesRX or \
			trafficData['lastBytesTX'] >= currBytesTX or \
			trafficData['lastBytesRX'] == 0 or \
			trafficData['lastBytesTX'] == 0:
			avgBytesRX = 0
			avgBytesTX = 0
			diffBytesRX = 0
			diffBytesTX = 0
		else:
			diffBytesRX = (currBytesRX - int(trafficData['lastBytesRX'])) 
			diffBytesTX = (currBytesTX - int(trafficData['lastBytesTX'])) 
			avgBytesRX = int( diffBytesRX / deltaTime)
			avgBytesTX = int( diffBytesTX / deltaTime)
		
		
		trafficData['avgBytesRX'] = avgBytesRX
		trafficData['lastBytesRX'] = currBytesRX
		trafficData['avgBytesTX'] = avgBytesTX
		trafficData['lastBytesTX'] = currBytesTX
		trafficData['timeLastCheck'] = time.time() 
		trafficDataFile['trafficData'] = trafficData
		trafficDataFile.close()
	else:
		trafficDataFile = shelve.open(trafficDataPath)
		trafficData = dict(	avgBytesRX = 0,
					lastBytesRX = 0, 
					avgBytesTX = 0, 
					lastBytesTX = 0,
					timeLastCheck = time.time() )
		trafficDataFile['trafficData'] = trafficData
		trafficDataFile.close()
	return trafficData

	
def doCheck(device):
	devData = getDevData(device)
	trafficData = processData(device, devData)

	if devData is not False:
		textOutput = str("OK - device " + device + " " + 
				" avgBytesRX " + str(trafficData['avgBytesRX']) +
				" avgBytesTX " + str(trafficData['avgBytesTX']) +
				" |" +  
				" avgBytesRX=" + str(trafficData['avgBytesRX']) +
				" avgBytesTX=" + str(trafficData['avgBytesTX'])	)
		returnCode = 0
	else:
		textOutput = 'CRITICAL - device ' + device + ' not found'
		returnCode = 2
	print(textOutput)
	return returnCode


if __name__ == '__main__':
	sys.exit(main())
