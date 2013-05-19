#!/usr/bin/python2

import sys
import os
import re
import shelve

def main():
	tmppath = '/tmp/check_cpu'
	cpustat = getCpu()
	if cpustat is not False:
		if os.path.isfile(tmppath):
			old_cpustat = loadData(tmppath)	
			saveData(cpustat, tmppath)
			cpustat = getDiff(cpustat, old_cpustat)
		else:
			saveData(cpustat, tmppath)
		cpustat = convertToPercentage(cpustat) 
	return exitCheck(cpustat)

def saveData(data, path):
	store = shelve.open(path)
	store['data'] = data
	store.close()


def loadData(path):
	store = shelve.open(path)
	data = store['data']
	store.close()
	return data	

def exitCheck(cpustat):
	if cpustat is False:
		output = 'UNKNOWN: Something went wrong.'	
		returnCode = 3
	else:
		output = 'CPU: user %s%%, nice %s%%, system %s%%, idle %s%%, iowait %s%%, irq %s%%, softirq %s%% | user=%s nice=%s system=%s idle=%s iowait=%s irq=%s softirq=%s' % (cpustat['user'], cpustat['nice'], cpustat['system'], cpustat['idle'], cpustat['iowait'], cpustat['irq'], cpustat['softirq'], cpustat['user'], cpustat['nice'], cpustat['system'], cpustat['idle'], cpustat['iowait'], cpustat['irq'], cpustat['softirq']) 
		returnCode = 0
			
	print output
	return returnCode
	

def getCpu(cpustat = dict()):
	stat_path = '/proc/stat'
	cpustat['user'] = 0
	cpustat['nice'] = 0
	cpustat['system'] = 0
	cpustat['idle'] = 0
	cpustat['iowait'] = 0
	cpustat['irq'] = 0
	cpustat['softirq'] = 0
	
	try:
		cpu = open(stat_path).readlines()
	except Exception, e:
		return False

	for line in cpu:
		if (re.match('^cpu.*', line)):
			line = re.sub('\s{1,}', ' ', line)
			cpustat['user'] = cpustat['user'] + int(line.split()[1])
			cpustat['nice'] = cpustat['nice'] + int(line.split()[2])
			cpustat['system'] = cpustat['system'] + int(line.split()[3])
			cpustat['idle'] = cpustat['idle'] + int(line.split()[4])
			cpustat['iowait'] = cpustat['iowait'] + int(line.split()[5])
			cpustat['irq'] = cpustat['irq'] + int(line.split()[6])
			cpustat['softirq'] = cpustat['softirq'] + int(line.split()[7])
	return cpustat

def convertToPercentage(cpustat):
	complete = 0
	for data in cpustat.iteritems():
		complete += data[1] 
	for value in cpustat.iteritems():
		cpustat[value[0]] = round(float(value[1]) / complete, 4) * 100

	return cpustat
	

def getDiff(cpustat, old_cpustat):
	for value in cpustat.iteritems():
		cpustat[value[0]] = cpustat[value[0]] - old_cpustat[value[0]]
	return cpustat

if __name__ == '__main__':
        sys.exit(main())

