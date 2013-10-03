<?php
$vertlabel = "Temperature and Humidity";

$opt[1] = '';
$def[1] = '';

$opt[1] .= " --imgformat=PNG --title=\" $hostname / " . $this->MACRO['DISP_SERVICEDESC'] . "\" --base=1024 --vertical-label=\"$vertlabel\" --slope-mode -l 0 ";

$def[1] .= "DEF:ds1=$RRDFILE[1]:$DS[1]:AVERAGE " ;
$def[1] .= "CDEF:temp=ds1 ";

$def[1] .= rrd::gradient('temp','FFFFFF','FF9EA5',"",20);
$def[1] .= "LINE2:temp" . "#FF0000" . "FF:\"$NAME[1]\t\" " ;
$def[1] .= "GPRINT:temp:LAST:\"Cur\\:%8.2lf $UNIT[1]\" ";
$def[1] .= "GPRINT:temp:AVERAGE:\"Avg\\:%8.2lf $UNIT[1]\" ";
$def[1] .= "GPRINT:temp:MIN:\"Min\\:%8.2lf $UNIT[1]\" ";
$def[1] .= "GPRINT:temp:MAX:\"Max\\:%8.2lf $UNIT[1]\\n\" ";

$opt[2] = '';
$def[2] = '';

$opt[2] .= " --imgformat=PNG --title=\" $hostname / " . $this->MACRO['DISP_SERVICEDESC'] . "\" --base=1024 --vertical-label=\"$vertlabel\" --slope-mode -l 0 ";

$def[2] .= "DEF:ds1=$RRDFILE[2]:$DS[2]:AVERAGE " ;
$def[2] .= "CDEF:hum=ds1 ";

$def[2] .= rrd::gradient('hum','#FFFFFF','#9EA5FF',"",20);
$def[2] .= "LINE2:hum" . "#0000FF" . "FF:\"$NAME[2]\t\" " ;
$def[2] .= "GPRINT:hum:LAST:\"Cur\\:%8.2lf $UNIT[2]\" ";
$def[2] .= "GPRINT:hum:AVERAGE:\"Avg\\:%8.2lf $UNIT[2]\" ";
$def[2] .= "GPRINT:hum:MIN:\"Min\\:%8.2lf $UNIT[2]\" ";
$def[2] .= "GPRINT:hum:MAX:\"Max\\:%8.2lf $UNIT[2]\\n\" ";
?>
