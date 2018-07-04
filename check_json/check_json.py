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

import sys
import json
import urllib.request
import argparse


def main():
    parser = argparse.ArgumentParser(
        description='Monitoring plugin to check a json value')
    parser.add_argument(
        '-n', '--name', required=True, help='value to check')
    parser.add_argument(
        '-u', '--url', required=True, help='url')
    parser.add_argument(
        '-w', '--warning', required=False, help='warning threshold', type=int)
    parser.add_argument(
        '-c', '--critical', required=False, help='critical threshold',
        type=int)
    args = parser.parse_args()

    name = args.name
    url = args.url
    warning = args.warning
    critical = args.critical

    status = 0
    try:
        response = urllib.request.urlopen(url)
    except urllib.request.HTTPError as e:
        print(e)
        sys.exit(1)
    json_object = response.read().decode()
    response_dict = json.loads(json_object)
    value = response_dict[name]
    if value >= critical:
        status = 2
    elif value >= warning:
        status = 1
    elif not value:
        status = 3
    msg = "Value %s: %s | value=%s;%s;%s" % (
        name, value, value, warning, critical)
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
