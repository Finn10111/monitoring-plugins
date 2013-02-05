#!/bin/bash
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
	unset $TEMP
fi

echo "$STATUSMSG: Temperature $TEMP °C, CPU Frequency $CPU | temp=$TEMP;$TEMPWARN;$TEMPCRIT cpu=$CPU"

exit $RETURNCODE
