#!/usr/bin/env python2

import sys
import os
import re
import shelve
import argparse

OK = 0
WARNING = 1
CRITICAL = 2
UNKNOWN = 3


def main():
    parser = argparse.ArgumentParser(description='Monitoring plugin for\
        checking linux cpu usage')
    parser.add_argument('-w', '--warning', required=False, type=float,
                        help='warning treshold for total cpu usage')
    parser.add_argument('-c', '--critical', required=False, type=float,
                        help='critical treshold for total cpu usage')
    args = parser.parse_args()
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
    return exitCheck(cpustat, args.warning, args.critical)


def saveData(data, path):
    store = shelve.open(path)
    store['data'] = data
    store.close()


def loadData(path):
    store = shelve.open(path)
    data = store['data']
    store.close()
    return data


def exitCheck(cpustat, warning, critical):
    if cpustat is False:
        prefix = 'UNKNOWN'
        status = UNKNOWN
    else:
        status = OK
        prefix = 'OK'
        total_usage = 100 - cpustat['idle']
        if total_usage > critical and critical is not None:
            status = CRITICAL
            prefix = 'CRITICAL'
        elif total_usage > warning and warning is not None:
            status = WARNING
            prefix = 'WARNING'
        output = """: CPU usage - user %(user)s%%, nice %(nice)s%%, \
system %(system)s%%, idle %(idle)s%%, iowait %(iowait)s%%, irq %(irq)s%%, \
softirq %(softirq)s%%, steal %(steal)s%%, guest %(guest)s%%, guest_nice \
%(guest_nice)s%%| user=%(user)s nice=%(nice)s system=%(system)s \
idle=%(idle)s iowait=%(iowait)s irq=%(irq)s softirq=%(softirq)s \
steal=%(steal)s guest=%(guest)s guest_nice=%(guest_nice)s """ % cpustat
    print prefix + output
    return status


def getCpu(cpustat=dict()):
    stat_path = '/proc/stat'
    cpustat['user'] = 0
    cpustat['nice'] = 0
    cpustat['system'] = 0
    cpustat['idle'] = 0
    cpustat['iowait'] = 0
    cpustat['irq'] = 0
    cpustat['softirq'] = 0
    cpustat['steal'] = 0
    cpustat['guest'] = 0
    cpustat['guest_nice'] = 0

    try:
        cpu = open(stat_path).readlines()
    except Exception, e:
        return False

    for line in cpu:
        if (re.match('^cpu.*', line)):
            line = re.sub('\s{1,}', ' ', line)
            values = line.split()
            cpustat['user'] = cpustat['user'] + int(values[1])
            cpustat['nice'] = cpustat['nice'] + int(values[2])
            cpustat['system'] = cpustat['system'] + int(values[3])
            cpustat['idle'] = cpustat['idle'] + int(values[4])
            cpustat['iowait'] = cpustat['iowait'] + int(values[5])
            cpustat['irq'] = cpustat['irq'] + int(values[6])
            cpustat['softirq'] = cpustat['softirq'] + int(values[7])
            if len(values) > 9:
                cpustat['steal'] = cpustat['steal'] + int(values[8])
            if len(values) > 10:
                cpustat['guest'] = cpustat['guest'] + int(values[9])
            if len(values) > 11:
                cpustat['guest_nice'] = cpustat['guest_nice'] + int(values[10])
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
