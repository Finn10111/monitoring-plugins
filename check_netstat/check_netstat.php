<?php
$vertlabel = "netstat connection statistics";

$opt[1] = '';
$def[1] = '';

$opt[1] .= " --imgformat=PNG --title=\" $hostname / " . $this->MACRO['DISP_SERVICEDESC'] . "\" --base=1024 --vertical-label=\"$vertlabel\" --slope-mode -l 0 ";

$def[1] .= "DEF:ds1=$RRDFILE[1]:$DS[1]:AVERAGE " ;
$def[1] .= "DEF:ds2=$RRDFILE[2]:$DS[2]:AVERAGE " ;
$def[1] .= "DEF:ds3=$RRDFILE[3]:$DS[3]:AVERAGE " ;
$def[1] .= "CDEF:sum_conns=ds1 ";
$def[1] .= "CDEF:tcp_conns=ds2 ";
$def[1] .= "CDEF:udp_conns=ds3 ";

$def[1] .= "LINE1:sum_conns" . "#000000" . "FF:\"$NAME[1]\t\" " ;
$def[1] .= "GPRINT:sum_conns:LAST:\"Cur\\:%8.2lf $UNIT[1]\" ";
$def[1] .= "GPRINT:sum_conns:AVERAGE:\"Avg\\:%8.2lf $UNIT[1]\" ";
$def[1] .= "GPRINT:sum_conns:MIN:\"Min\\:%8.2lf $UNIT[1]\" ";
$def[1] .= "GPRINT:sum_conns:MAX:\"Max\\:%8.2lf $UNIT[1]\\n\" ";

$def[1] .= "LINE1:tcp_conns" . "#0000FF" . "FF:\"$NAME[2]\t\" " ;
$def[1] .= "GPRINT:tcp_conns:LAST:\"Cur\\:%8.2lf $UNIT[2]\" ";
$def[1] .= "GPRINT:tcp_conns:AVERAGE:\"Avg\\:%8.2lf $UNIT[2]\" ";
$def[1] .= "GPRINT:tcp_conns:MIN:\"Min\\:%8.2lf $UNIT[2]\" ";
$def[1] .= "GPRINT:tcp_conns:MAX:\"Max\\:%8.2lf $UNIT[2]\\n\" ";

$def[1] .= "LINE1:udp_conns" . "#00CC00" . "FF:\"$NAME[3]\t\" " ;
$def[1] .= "GPRINT:udp_conns:LAST:\"Cur\\:%8.2lf $UNIT[3]\" ";
$def[1] .= "GPRINT:udp_conns:AVERAGE:\"Avg\\:%8.2lf $UNIT[3]\" ";
$def[1] .= "GPRINT:udp_conns:MIN:\"Min\\:%8.2lf $UNIT[3]\" ";
$def[1] .= "GPRINT:udp_conns:MAX:\"Max\\:%8.2lf $UNIT[3]\\n\" ";


?>

