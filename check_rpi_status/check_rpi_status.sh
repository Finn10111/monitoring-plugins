#!/bin/bash
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

RETURNCODE=0
STATUSMSG=OK

TEMPFILE=/sys/class/thermal/thermal_zone0/temp
CPUFILE=/sys/bus/cpu/devices/cpu0/cpufreq/cpuinfo_cur_freq
TEMPWARN=70
TEMPCRIT=80

TEMP=$(cat $TEMPFILE)
if [ $? != 0 ]; then
	RETURNCODE=3
	STATUSMSG=UNKNOWN
fi

CPU=$(cat $CPUFILE)
if [ $? != 0 ]; then
	RETURNCODE=3
	STATUSMSG=UNKNOWN
fi 

TEMP=$[$TEMP / 1000]
CPU=$[$CPU / 1000]

if [ $TEMP -gt $TEMPWARN ]; then
	RETURNCODE=1
	STATUSMSG=WARNING
fi	

if [ $TEMP -gt $TEMPCRIT ]; then
	RETURNCODE=2
	STATUSMSG=CRITICAL
fi

if [ $TEMP -lt 0 ]; then
	RETURNCODE=3
	STATUSMSG=UNKNOWN
	$TEMP=0
fi

echo "$STATUSMSG: Temperature $TEMP °C, CPU Frequency $CPU | temp=$TEMP;$TEMPWARN;$TEMPCRIT cpu=$CPU"

exit $RETURNCODE
