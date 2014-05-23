#!/usr/bin/env python
import sys
import re
import os
import time
import subprocess
import argparse
import shelve

class PowerDNSStats:
    __warning = False
    __critical = False
    __store_path = '/tmp/check_pdns'
    __values = ['packetcache-hit', 'packetcache-miss', 'query-cache-hit', 'query-cache-miss', 'recursing-answers', 'recursing-questions', 'corrupt-packets', 'servfail-packets', 'timedout-packets']
    __data = dict()

    def __init__(self, warning=False, critical=False):
        self.__warning = int(warning)
        self.__critical = int(critical)

    def __is_first_run(self):
	if not os.path.isfile(self.__store_path):
	    self.__getData()
	    self.__setData()
            return True
        else:
            return False

    def __getData(self):
        self.__data = self.__call_pdns__()
        self.__data['timeLastCheck'] = time.time()
        return self.__data


    def __setData(self):
        pluginStore = shelve.open(self.__store_path)
        pluginStore['pluginData'] = self.__data
        pluginStore.close()
        return True


    def __getStoredData(self):
        pluginDataFile = shelve.open(self.__store_path)
        pluginData = pluginDataFile['pluginData']
        pluginDataFile.close()
        return pluginData


    def __calcDiff(self, new_values, old_values):
        diff = new_values
        timediff = int(new_values['timeLastCheck']) - int(old_values['timeLastCheck'])
        for key in new_values:
            diff_value = (float(new_values[key]) - float(old_values[key])) / timediff
            if diff_value >= 0 and diff != False:
                diff[key] = diff_value
            else:
                diff = False
        return diff



    def run(self):
        if not self.__is_first_run():
            new_values = self.__getData()
            old_values = self.__getStoredData()
            self.__setData()
            diff = self.__calcDiff(new_values, old_values)
            return self.__exit__(diff)
        else:
            return self.__exit__(False)


    def __call_pdns__(self):
        pdns_output = subprocess.Popen('LANG=en_EN.utf8 /usr/bin/sudo /usr/bin/pdns_control show "*"', shell=True,
                stdout=subprocess.PIPE).communicate()[0]
        return self.__process_pdns_output__(pdns_output)


    def __process_pdns_output__(self, pdns_output):
        for key in self.__values:
            value = re.search(key+'=?(\d*)', pdns_output).group(1)
            self.__data[key] = value

        return self.__data


    def __exit__(self, diff=False):
        if diff == False:
            return_code = 3
            prefix = "UNKNOWN:"
            output = prefix + ' Collecting data for first time run'
        else:
            return_code = 0
            prefix = "OK:"
            output = prefix + " statistics read | "

            for key in diff:
                if key != 'timeLastCheck':
                    output += key + '=' + '%.3f' % diff[key] + ' '


        print output
        return return_code




def main():
    parser = argparse.ArgumentParser(description = 'Nagios plugin to check pdns statistics')
    thresholds = parser.add_argument_group('thresholds', 'warning and critical thresholds for total number of connections')
    thresholds.add_argument('-w', '--warning', required=False, default=False,
            type=int)
    thresholds.add_argument('-c', '--critical', required=False, default=False,
            type=int)
    args = parser.parse_args()

    powerdns_stats = PowerDNSStats(args.warning, args.critical)
    return powerdns_stats.run()


if __name__ == '__main__':
    sys.exit(main())

