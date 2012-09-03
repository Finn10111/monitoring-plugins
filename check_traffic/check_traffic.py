#!/usr/bin/python
""" Description...
..................
.................."""
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
	trafficDataPath = '/tmp/check_traffic_'+device
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
		totalBytesRX = int(trafficData['totalBytesRX']) + diffBytesRX
		totalBytesTX = int(trafficData['totalBytesTX']) + diffBytesTX
		
		
		trafficData['avgBytesRX'] = avgBytesRX
		trafficData['lastBytesRX'] = currBytesRX
		trafficData['avgBytesTX'] = avgBytesTX
		trafficData['lastBytesTX'] = currBytesTX
		trafficData['totalBytesRX'] = totalBytesRX
		trafficData['totalBytesTX'] = totalBytesTX
		trafficData['timeLastCheck'] = time.time() 
		trafficDataFile['trafficData'] = trafficData
		trafficDataFile.close()
	else:
		trafficDataFile = shelve.open(trafficDataPath)
		trafficData = dict(	avgBytesRX = 0,
					lastBytesRX = 0, 
					avgBytesTX = 0, 
					lastBytesTX = 0,
					totalBytesRX = 0, 
					totalBytesTX = 0, 
					timeLastCheck = time.time() )
		trafficDataFile['trafficData'] = trafficData
		trafficDataFile.close()
	return trafficData
	
def doCheck(device):
	devData = getDevData(device)
	trafficData = processData(device, devData)

	if devData is not False:
		textOutput = str("OK - device " + device + " |" +  
				" avgBytesRX=" + str(trafficData['avgBytesRX']) +
				" avgBytesTX=" + str(trafficData['avgBytesTX']) +
				" totalBytesRX=" + str(trafficData['totalBytesRX']) +
				" totalBytesTX=" + str(trafficData['totalBytesTX']) 
				)
		returnCode = 0
	else:
		textOutput = 'CRITICAL - device ' + device + ' not found'
		returnCode = 2
	print(textOutput)
	return returnCode

if __name__ == '__main__':
	sys.exit(main())


	 

