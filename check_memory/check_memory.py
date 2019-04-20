#!/usr/bin/env python3
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

import sys
import re
import argparse


def main():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-w', '--warning', required=False, type=int,
                        help='warning in %')
    parser.add_argument('-c', '--critical', required=False, type=int,
                        help='ctitical in %')
    args = parser.parse_args()

    warning = args.warning
    critical = args.critical

    memory = getMemory()

    status = "OK"
    exit_code = 0

    if memory['totalfree'] <= warning:
        exit_code = 1
        status = "WARNING"

    if memory['totalfree'] <= critical:
        exit_code = 2
        status = "CRITICAL"

    totalfree = round((memory['totalfree'] / memory['total'] * 100), 1)
    free = round((memory['free'] / memory['total'] * 100), 1)
    status_values = {
            'totalfree': totalfree,
            'free': free
        }
    status_text = ': Memory free: %(totalfree)s %% \
(%(free)s %% including buffers/cached)' % status_values
    status += status_text
    print(status)
    return exit_code


def getMemory():
    try:
        memory = open('/proc/meminfo').read()
        total = int(re.search(r'(MemTotal:)(\s*)(\d*)', memory,
                              re.M).group(3)) * 1000
        free = int(re.search(r'(MemFree:)(\s*)(\d*)', memory,
                             re.M).group(3)) * 1000
        buffers = int(re.search(r'(Buffers:)(\s*)(\d*)', memory,
                                re.M).group(3)) * 1000
        cached = int(re.search(r'(Cached:)(\s*)(\d*)', memory,
                               re.M).group(3)) * 1000
        swapcached = int(re.search(r'(SwapCached:)(\s*)(\d*)', memory,
                                   re.M).group(3)) * 1000
        used = total - free - buffers - cached
        totalfree = float(total - used)
    except Exception:
        print("UNKNOWN Could not read /proc/meminfo")
        sys.exit(3)

    memory_values = {
        'total': total,
        'used': used,
        'free': free,
        'totalfree': totalfree,
        'buffers': buffers,
        'cached': cached,
        'swapcached': swapcached
    }
    return memory_values


if __name__ == '__main__':
    sys.exit(main())
