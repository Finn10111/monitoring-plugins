<?php
$vertlabel = "stats per second";

$opt[1] = '';
$def[1] = '';

$opt[1] .= " --imgformat=PNG --title=\" $hostname / " . $this->MACRO['DISP_SERVICEDESC'] . "\" --base=1024 --vertical-label=\"$vertlabel\" --slope-mode -l 0 ";

$def[1] .= "DEF:ds1=$RRDFILE[1]:$DS[1]:AVERAGE " ;
$def[1] .= "DEF:ds2=$RRDFILE[2]:$DS[2]:AVERAGE " ;
$def[1] .= "DEF:ds8=$RRDFILE[8]:$DS[8]:AVERAGE " ;
$def[1] .= "DEF:ds9=$RRDFILE[9]:$DS[9]:AVERAGE " ;
$def[1] .= "CDEF:servfail-packets=ds1 ";
$def[1] .= "CDEF:corrupt-packets=ds8 ";
$def[1] .= "CDEF:timedout-packets=ds9 ";
$def[1] .= "CDEF:udp-queries=ds2 ";

$def[1] .= "LINE1:servfail-packets" . "#FF0000" . "FF:\"$NAME[1]\t\" " ;
$def[1] .= "GPRINT:servfail-packets:LAST:\"Cur\\:%8.2lf $UNIT[1]\" ";
$def[1] .= "GPRINT:servfail-packets:AVERAGE:\"Avg\\:%8.2lf $UNIT[1]\" ";
$def[1] .= "GPRINT:servfail-packets:MIN:\"Min\\:%8.2lf $UNIT[1]\" ";
$def[1] .= "GPRINT:servfail-packets:MAX:\"Max\\:%8.2lf $UNIT[1]\\n\" ";

$def[1] .= "LINE1:corrupt-packets" . "#00FF00" . "FF:\"$NAME[8]\t\" " ;
$def[1] .= "GPRINT:corrupt-packets:LAST:\"Cur\\:%8.2lf $UNIT[8]\" ";
$def[1] .= "GPRINT:corrupt-packets:AVERAGE:\"Avg\\:%8.2lf $UNIT[8]\" ";
$def[1] .= "GPRINT:corrupt-packets:MIN:\"Min\\:%8.2lf $UNIT[8]\" ";
$def[1] .= "GPRINT:corrupt-packets:MAX:\"Max\\:%8.2lf $UNIT[8]\\n\" ";

$def[1] .= "LINE1:timedout-packets" . "#0000FF" . "FF:\"$NAME[9]\t\" " ;
$def[1] .= "GPRINT:timedout-packets:LAST:\"Cur\\:%8.2lf $UNIT[9]\" ";
$def[1] .= "GPRINT:timedout-packets:AVERAGE:\"Avg\\:%8.2lf $UNIT[9]\" ";
$def[1] .= "GPRINT:timedout-packets:MIN:\"Min\\:%8.2lf $UNIT[9]\" ";
$def[1] .= "GPRINT:timedout-packets:MAX:\"Max\\:%8.2lf $UNIT[9]\\n\" ";

$def[1] .= "LINE1:udp-queries" . "#000000" . "FF:\"$NAME[2]\t\t\" " ;
$def[1] .= "GPRINT:udp-queries:LAST:\"Cur\\:%8.2lf $UNIT[2]\" ";
$def[1] .= "GPRINT:udp-queries:AVERAGE:\"Avg\\:%8.2lf $UNIT[2]\" ";
$def[1] .= "GPRINT:udp-queries:MIN:\"Min\\:%8.2lf $UNIT[2]\" ";
$def[1] .= "GPRINT:udp-queries:MAX:\"Max\\:%8.2lf $UNIT[2]\\n\" ";

$opt[2] = '';
$def[2] = '';

$opt[2] .= " --imgformat=PNG --title=\" $hostname / " . $this->MACRO['DISP_SERVICEDESC'] . "\" --base=1024 --vertical-label=\"$vertlabel\" --slope-mode -l 0 ";

$def[2] .= "DEF:ds3=$RRDFILE[3]:$DS[3]:AVERAGE " ;
$def[2] .= "DEF:ds4=$RRDFILE[4]:$DS[4]:AVERAGE " ;
$def[2] .= "DEF:ds5=$RRDFILE[5]:$DS[5]:AVERAGE " ;
$def[2] .= "DEF:ds6=$RRDFILE[6]:$DS[6]:AVERAGE " ;
$def[2] .= "DEF:ds7=$RRDFILE[7]:$DS[7]:AVERAGE " ;
$def[2] .= "DEF:ds10=$RRDFILE[10]:$DS[10]:AVERAGE " ;
$def[2] .= "CDEF:query-cache-hit=ds3 ";
$def[2] .= "CDEF:recursing-answers=ds4 ";
$def[2] .= "CDEF:packetcache-hit=ds5 ";
$def[2] .= "CDEF:recursing-questions=ds6 ";
$def[2] .= "CDEF:query-cache-miss=ds7 ";
$def[2] .= "CDEF:packetcache-miss=ds10 ";

$def[2] .= "LINE1:query-cache-hit" . "#009900" . "FF:\"$NAME[3]\t\" " ;
$def[2] .= "GPRINT:query-cache-hit:LAST:\"Cur\\:%8.2lf $UNIT[3]\" ";
$def[2] .= "GPRINT:query-cache-hit:AVERAGE:\"Avg\\:%8.2lf $UNIT[3]\" ";
$def[2] .= "GPRINT:query-cache-hit:MIN:\"Min\\:%8.2lf $UNIT[3]\" ";
$def[2] .= "GPRINT:query-cache-hit:MAX:\"Max\\:%8.2lf $UNIT[3]\\n\" ";

$def[2] .= "LINE1:query-cache-miss" . "#99FF99" . "FF:\"$NAME[7]\t\" " ;
$def[2] .= "GPRINT:query-cache-miss:LAST:\"Cur\\:%8.2lf $UNIT[7]\" ";
$def[2] .= "GPRINT:query-cache-miss:AVERAGE:\"Avg\\:%8.2lf $UNIT[7]\" ";
$def[2] .= "GPRINT:query-cache-miss:MIN:\"Min\\:%8.2lf $UNIT[7]\" ";
$def[2] .= "GPRINT:query-cache-miss:MAX:\"Max\\:%8.2lf $UNIT[7]\\n\" ";

$def[2] .= "LINE1:packetcache-hit" . "#000099" . "FF:\"$NAME[5]\t\" " ;
$def[2] .= "GPRINT:packetcache-hit:LAST:\"Cur\\:%8.2lf $UNIT[5]\" ";
$def[2] .= "GPRINT:packetcache-hit:AVERAGE:\"Avg\\:%8.2lf $UNIT[5]\" ";
$def[2] .= "GPRINT:packetcache-hit:MIN:\"Min\\:%8.2lf $UNIT[5]\" ";
$def[2] .= "GPRINT:packetcache-hit:MAX:\"Max\\:%8.2lf $UNIT[5]\\n\" ";

$def[2] .= "LINE1:packetcache-miss" . "#9999FF" . "FF:\"$NAME[10]\t\" " ;
$def[2] .= "GPRINT:packetcache-miss:LAST:\"Cur\\:%8.2lf $UNIT[10]\" ";
$def[2] .= "GPRINT:packetcache-miss:AVERAGE:\"Avg\\:%8.2lf $UNIT[10]\" ";
$def[2] .= "GPRINT:packetcache-miss:MIN:\"Min\\:%8.2lf $UNIT[10]\" ";
$def[2] .= "GPRINT:packetcache-miss:MAX:\"Max\\:%8.2lf $UNIT[10]\\n\" ";


$def[2] .= "LINE1:recursing-questions" . "#990000" . "FF:\"".substr_replace($NAME[6], '', 17)."\t\" " ;
$def[2] .= "GPRINT:recursing-questions:LAST:\"Cur\\:%8.2lf $UNIT[6]\" ";
$def[2] .= "GPRINT:recursing-questions:AVERAGE:\"Avg\\:%8.2lf $UNIT[6]\" ";
$def[2] .= "GPRINT:recursing-questions:MIN:\"Min\\:%8.2lf $UNIT[6]\" ";
$def[2] .= "GPRINT:recursing-questions:MAX:\"Max\\:%8.2lf $UNIT[6]\\n\" ";

$def[2] .= "LINE1:recursing-answers" . "#FF9999" . "FF:\"$NAME[4]\t\" " ;
$def[2] .= "GPRINT:recursing-answers:LAST:\"Cur\\:%8.2lf $UNIT[4]\" ";
$def[2] .= "GPRINT:recursing-answers:AVERAGE:\"Avg\\:%8.2lf $UNIT[4]\" ";
$def[2] .= "GPRINT:recursing-answers:MIN:\"Min\\:%8.2lf $UNIT[4]\" ";
$def[2] .= "GPRINT:recursing-answers:MAX:\"Max\\:%8.2lf $UNIT[4]\\n\" ";



?>

