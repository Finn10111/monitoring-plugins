<?php
 
$vertlabel = "Memory";
 
$opt[1] = '';
$def[1] = '';
 
$opt[1] .= " --imgformat=PNG --title=\" $hostname / " . $this->MACRO['DISP_SERVICEDESC'] . "\" --base=1024 --vertical-label=\"$vertlabel\" --slope-mode -l 0 ";
 
$def[1] .= "DEF:ds1=$RRDFILE[1]:$DS[1]:AVERAGE " ;
$def[1] .= "DEF:ds2=$RRDFILE[2]:$DS[2]:AVERAGE " ;
$def[1] .= "DEF:ds3=$RRDFILE[3]:$DS[3]:AVERAGE " ;
$def[1] .= "DEF:ds4=$RRDFILE[4]:$DS[4]:AVERAGE " ;
$def[1] .= "DEF:ds5=$RRDFILE[5]:$DS[5]:AVERAGE " ;
$def[1] .= "DEF:ds6=$RRDFILE[6]:$DS[6]:AVERAGE " ;
$def[1] .= "DEF:ds7=$RRDFILE[7]:$DS[7]:AVERAGE " ;
$def[1] .= "CDEF:total=ds1 ";
$def[1] .= "CDEF:free=ds2 ";
$def[1] .= "CDEF:totalfree=ds3 ";
$def[1] .= "CDEF:used=ds4 ";
$def[1] .= "CDEF:buffers=ds5 ";
$def[1] .= "CDEF:cached=ds6 ";
$def[1] .= "CDEF:swapcached=ds7 ";


$def[1] .= "AREA:used" . "#FF0000" . "FF:\"$NAME[4]\t\" " ;
$def[1] .= "GPRINT:used:LAST:\"Cur\\:%8.2lf $UNIT[4]\" ";
$def[1] .= "GPRINT:used:AVERAGE:\"Avg\\:%8.2lf $UNIT[4]\" ";
$def[1] .= "GPRINT:used:MAX:\"Max\\:%8.2lf $UNIT[4]\\n\" ";
 
$def[1] .= "AREA:buffers" . "#7700FF" . "FF:\"$NAME[5]\t\":STACK " ;
$def[1] .= "GPRINT:buffers:LAST:\"Cur\\:%8.2lf $UNIT[5]\" ";
$def[1] .= "GPRINT:buffers:AVERAGE:\"Avg\\:%8.2lf $UNIT[5]\" ";
$def[1] .= "GPRINT:buffers:MAX:\"Max\\:%8.2lf $UNIT[5]\\n\" ";

$def[1] .= "AREA:cached" . "#33BBFF" . "FF:\"$NAME[6]\t\":STACK " ;
$def[1] .= "GPRINT:cached:LAST:\"Cur\\:%8.2lf $UNIT[6]\" ";
$def[1] .= "GPRINT:cached:AVERAGE:\"Avg\\:%8.2lf $UNIT[6]\" ";
$def[1] .= "GPRINT:cached:MAX:\"Max\\:%8.2lf $UNIT[6]\\n\" ";



$def[1] .= "AREA:free" . "#00FF00" . "FF:\"$NAME[2]\t\":STACK " ;
$def[1] .= "GPRINT:free:LAST:\"Cur\\:%8.2lf $UNIT[2]\" ";
$def[1] .= "GPRINT:free:AVERAGE:\"Avg\\:%8.2lf $UNIT[2]\" ";
$def[1] .= "GPRINT:free:MAX:\"Max\\:%8.2lf $UNIT[2]\\n\" ";
 
 
 
 
 
$def[1] .= "LINE1:total" . "#000000" . "FF:\"$NAME[1]\t\" ";
$def[1] .= "GPRINT:total:LAST:\"Cur\\:%8.2lf $UNIT[1]\" ";
$def[1] .= "GPRINT:total:AVERAGE:\"Avg\\:%8.2lf $UNIT[1]\" ";
$def[1] .= "GPRINT:total:MAX:\"Max\\:%8.2lf $UNIT[1]\\n\" ";
 
 
# warning and critial thresholds not implemented in check yet
 
#if (isset($WARN[1]) &amp;&amp; $WARN[1] != "") {
#$def[1] .= "HRULE:$WARN[1]#FFFF00:\"Warning ($NAME[1])\: " . $WARN[1] . " " . $UNIT[1] . " \\n\" " ;
#}
#
#if (isset($CRIT[1]) &amp;&amp; $CRIT[1] != "") {
#$def[1] .= "HRULE:$CRIT[1]#FF0000:\"Critical ($NAME[1])\: " . $CRIT[1] . " " . $UNIT[1] . " \\n\" " ;
#}

?>
