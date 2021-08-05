#!/usr/bin/python3
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
# https://github.com/UedaTakeyuki/mh-z19
# pip3 install mh-z19

import sys
import mh_z19
import argparse


def main():
    parser = argparse.ArgumentParser(
        description='Monitoring plugin to check mhz19 co2 sensor')
    parser.add_argument(
        '-w', '--warning', required=False, help='warning threshold', type=int)
    parser.add_argument(
        '-c', '--critical', required=False, help='critical threshold',
        type=int)
    args = parser.parse_args()

    warning = args.warning
    critical = args.critical

    status = 0
    values = mh_z19.read_all()
    value = values['co2']

    if warning and critical:
        if value >= critical:
            status = 2
        elif value >= warning:
            status = 1
        elif not value:
            status = 3
    else:
        warning = 0
        critical = 0
    msg = "co2: %s | value=%s;%s;%s" % (
        value, value, warning, critical)
    # process thresholds
    exitCheck(status, msg)


def exitCheck(status, msg=''):
    if status == 0:
        msg = 'OK - ' + msg
    elif status == 1:
        msg = 'WARNING - ' + msg
    elif status == 2:
        msg = 'CRITICAL - ' + msg
    elif status == 3:
        msg = 'UNKNOWN - ' + msg
    print(msg)
    sys.exit(status)


if __name__ == '__main__':
    sys.exit(main())
