<?php
 
$vertlabel = "Memory";
 
$opt[1] = '';
$def[1] = '';
 
$opt[1] .= " --imgformat=PNG --title=\" $hostname / " . $this->MACRO['DISP_SERVICEDESC'] . "\" --base=1024 --vertical-label=\"$vertlabel\" --slope-mode -l 0 ";
 
$def[1] .= rrd::def('total', $RRDFILE[1], $DS[1], 'AVERAGE');
$def[1] .= rrd::def('free', $RRDFILE[2], $DS[2], 'AVERAGE');
$def[1] .= rrd::def('total_free', $RRDFILE[3], $DS[3], 'AVERAGE');
$def[1] .= rrd::def('used', $RRDFILE[4], $DS[4], 'AVERAGE');
$def[1] .= rrd::def('buffers', $RRDFILE[5], $DS[5], 'AVERAGE');
$def[1] .= rrd::def('cached', $RRDFILE[6], $DS[6], 'AVERAGE');
$def[1] .= rrd::def('swapcached', $RRDFILE[7], $DS[7], 'AVERAGE');

$def[1] .= rrd::area('used', '#FF0000', 'used    ' );
$def[1] .= rrd::gprint('used', array('LAST', 'MIN', 'MAX', 'AVERAGE'), '%6.2lf %s' );
 
$def[1] .= rrd::area('buffers', '#7700FF', 'buffers ', true );
$def[1] .= rrd::gprint('buffers', array('LAST', 'MIN', 'MAX', 'AVERAGE'), '%6.2lf %s' );

$def[1] .= rrd::area('cached', '#33BBFF', 'cached  ', true );
$def[1] .= rrd::gprint('cached', array('LAST', 'MIN', 'MAX', 'AVERAGE'), '%6.2lf %s' );

$def[1] .= rrd::area('free', '#00FF00', 'free    ', true );
$def[1] .= rrd::gprint('free', array('LAST', 'MIN', 'MAX', 'AVERAGE'), '%6.2lf %s' );
 
$def[1] .= rrd::line1('total', '#000000', 'total   ');
$def[1] .= rrd::gprint('total', array('LAST', 'MIN', 'MAX', 'AVERAGE'), '%6.2lf %s' );
 
# warning and critial thresholds not implemented in check yet
 
#if (isset($WARN[1]) &amp;&amp; $WARN[1] != "") {
#$def[1] .= "HRULE:$WARN[1]#FFFF00:\"Warning ($NAME[1])\: " . $WARN[1] . " " . $UNIT[1] . " \\n\" " ;
#}
#
#if (isset($CRIT[1]) &amp;&amp; $CRIT[1] != "") {
#$def[1] .= "HRULE:$CRIT[1]#FF0000:\"Critical ($NAME[1])\: " . $CRIT[1] . " " . $UNIT[1] . " \\n\" " ;
#}

?>
