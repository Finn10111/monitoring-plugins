<?php
 
$vertlabel = "Traffic";
 
$opt[1] = '';
$def[1] = '';
 
$opt[1] .= " --imgformat=PNG --title=\" $hostname / " . $this->MACRO['DISP_SERVICEDESC'] . "\" --base=1024 --vertical-label=\"$vertlabel\" --slope-mode ";
 
$def[1] .= "DEF:ds1=$RRDFILE[1]:$DS[1]:AVERAGE " ;
$def[1] .= "DEF:ds2=$RRDFILE[2]:$DS[2]:AVERAGE " ;
$def[1] .= "CDEF:var1=ds1 ";
$def[1] .= "CDEF:var2=ds2 ";
 
$def[1] .= "LINE1:var1" . "#00FF00" . "FF:\"$NAME[1]\t\" ";
$def[1] .= "AREA:var1" . "#00FF00FF ";
$def[1] .= "GPRINT:var1:LAST:\"Cur\\:%8.2lf $UNIT[1]\" ";
$def[1] .= "GPRINT:var1:AVERAGE:\"Avg\\:%8.2lf $UNIT[1]\" ";
$def[1] .= "GPRINT:var1:MAX:\"Max\\:%8.2lf $UNIT[1]\\n\" ";
 
$def[1] .= "LINE1:var2" . "#FF0000" . "FF:\"$NAME[2]\t\" ";
$def[1] .= "AREA:var2" . "#FF000066 ";
$def[1] .= "GPRINT:var2:LAST:\"Cur\\:%8.2lf $UNIT[2]\" ";
$def[1] .= "GPRINT:var2:AVERAGE:\"Avg\\:%8.2lf $UNIT[2]\" ";
$def[1] .= "GPRINT:var2:MAX:\"Max\\:%8.2lf $UNIT[2]\\n\" ";
 
 
# warning and critial thresholds not implemented in check yet
 
#if (isset($WARN[1]) &amp;&amp; $WARN[1] != "") {
#$def[1] .= "HRULE:$WARN[1]#FFFF00:\"Warning ($NAME[1])\: " . $WARN[1] . " " . $UNIT[1] . " \\n\" " ;
#}
#
#if (isset($CRIT[1]) &amp;&amp; $CRIT[1] != "") {
#$def[1] .= "HRULE:$CRIT[1]#FF0000:\"Critical ($NAME[1])\: " . $CRIT[1] . " " . $UNIT[1] . " \\n\" " ;
#}

?>
