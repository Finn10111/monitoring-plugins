#!/usr/bin/env python
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# You have to add these two lines with visudo to get this plugin working:
# Defaults:nrpe    !requiretty
# nrpe  ALL=NOPASSWD: /usr/bin/pdns_control
# The plugin stores some data in /tmp/check_pdns, if you have run it as a user
# which is not the monitoring user you have to delete the file so the
# monitoring user can read/write the file.
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
    __values = ['packetcache-hit', 'packetcache-miss', 'query-cache-hit', 'query-cache-miss', 'recursing-answers', 'recursing-questions', 'corrupt-packets', 'servfail-packets', 'timedout-packets', 'udp-queries', 'tcp-queries', 'qsize-q']
    __data = dict()

    def __init__(self, warning=False, critical=False, warningerr=False, criticalerr=False):
        self.__warning = float(warning)
        self.__critical = float(critical)
        self.__warningerr = float(warningerr)
        self.__criticalerr = float(criticalerr)

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
            try:
                diff_value = (float(new_values[key]) - float(old_values[key])) / timediff
                if diff_value >= 0 and diff != False:
                    diff[key] = diff_value
                else:
                    diff = False
            except ZeroDivisionError as e:
                diff = 'TooFast'
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
        return_code = 0
        prefix = "OK: "
        if diff == False:
            return_code = 3
            prefix = "UNKNOWN: "
            output = prefix + 'Collecting data for first time run'
        elif diff == "TooFast":
            return_code = 3
            prefix = "UNKNOWN: "
            output = prefix + 'Check can not be executed twice a second'
        else:
            # check if thresholds are set
            if self.__warningerr != False and self.__criticalerr != False:
                # check for critical errors
                if diff['corrupt-packets'] >= self.__criticalerr or diff['servfail-packets'] >= self.__criticalerr or diff['timedout-packets'] >= self.__criticalerr:
                    return_code = 2
                    prefix = "CRITICAL: "
                # check for warning errors
                elif diff['corrupt-packets'] >= self.__warningerr or diff['servfail-packets'] >= self.__warningerr or diff['timedout-packets'] >= self.__warningerr:
                    return_code = 1
                    prefix = "WARNING: "
            if self.__warning != False and self.__critical != False:
                # check for critical query count
                if (diff['udp-queries'] + diff['tcp-queries']) >= self.__critical:
                    return_code = 2
                    prefix = "CRITICAL: "
                # check for warning query count
                elif (diff['udp-queries'] + diff['tcp-queries']) >= self.__warning and return_code == 0:
                    return_code = 1
                    prefix = "WARNING: "

            output = prefix + 'Queries: %.3f/s udp-queries, %.3f/s tcp-queries, Error rates: %.3f/s servfail-packets, %.3f/s corrupt-packets, %.3f/s timedout-packets, Cache: %.3f/s packetcache-hit, %.3f/s packetcache-miss, %.3f/s query-cache-hit, %.3f/s query-cache-miss, Recursor: %.3f/s recursing-questions, %.3f/s recursing-answers' % (diff['udp-queries'], diff['tcp-queries'], diff['servfail-packets'], diff['corrupt-packets'], diff['timedout-packets'], diff['packetcache-hit'], diff['packetcache-miss'], diff['query-cache-hit'], diff['query-cache-miss'], diff['recursing-questions'], diff['recursing-answers']) + ' | '
            for key in diff:
                if key != 'timeLastCheck':
                    output += key + '=' + '%.3f' % diff[key] + ' '

        print output
        return return_code


def main():
    parser = argparse.ArgumentParser(description = 'Nagios plugin for monitoring PowerDNS')
    thresholds = parser.add_argument_group('query thresholds', 'warning and critical thresholds for queries per second')
    thresholds.add_argument('-w', '--warning', required=False, default=False,
            type=float, help='treshold for queries per second')
    thresholds.add_argument('-c', '--critical', required=False, default=False,
            type=float, help='treshold for queries per second')
    err_thresholds = parser.add_argument_group('error thresholds', 'warning and critical thresholds for errors per second')
    err_thresholds.add_argument('-W', '--warningerr', required=False, default=False,
            type=float, help='treshold for some kind of errors per second')
    err_thresholds.add_argument('-C', '--criticalerr', required=False, default=False,
            type=float, help='treshold for some kind of errors per second')
    args = parser.parse_args()

    powerdns_stats = PowerDNSStats(args.warning, args.critical, args.warningerr, args.criticalerr)
    return powerdns_stats.run()


if __name__ == '__main__':
    sys.exit(main())

