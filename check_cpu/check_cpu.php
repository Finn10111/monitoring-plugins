<?php
 
$vertlabel = "CPU";
 
$opt[1] = '';
$def[1] = '';
 
$opt[1] .= " --imgformat=PNG --title=\" $hostname / " . $this->MACRO['DISP_SERVICEDESC'] . "\" --base=1000 --vertical-label=\"$vertlabel\" --slope-mode -l 0 -u 100 --rigid ";
$def[1]	.= rrd::def('user', $RRDFILE[1], $DS[1], 'AVERAGE');
$def[1]	.= rrd::def('nice', $RRDFILE[2], $DS[2], 'AVERAGE');
$def[1]	.= rrd::def('system', $RRDFILE[3], $DS[3], 'AVERAGE');
$def[1]	.= rrd::def('idle', $RRDFILE[4], $DS[4], 'AVERAGE');
$def[1]	.= rrd::def('iowait', $RRDFILE[5], $DS[5], 'AVERAGE');
$def[1]	.= rrd::def('irq', $RRDFILE[6], $DS[6], 'AVERAGE');
$def[1]	.= rrd::def('softirq', $RRDFILE[7], $DS[7], 'AVERAGE');

$def[1] .= rrd::area('system', '#9f40ff', 'system  ', true );
$def[1] .= rrd::gprint('system', array('LAST', 'MIN', 'MAX', 'AVERAGE'), '%5.2lf %S' );

$def[1] .= rrd::area('user', '#40ffff', 'user    ', true );
$def[1] .= rrd::gprint('user', array('LAST', 'MIN', 'MAX', 'AVERAGE'), '%5.2lf %S' );

$def[1] .= rrd::area('nice', '#9fff40', 'nice    ', true );
$def[1] .= rrd::gprint('nice', array('LAST', 'MIN', 'MAX', 'AVERAGE'), '%5.2lf %S' );

$def[1] .= rrd::area('iowait', '#ff4040', 'iowait  ', true );
$def[1] .= rrd::gprint('iowait', array('LAST', 'MIN', 'MAX', 'AVERAGE'), '%5.2lf %S' );

$def[1] .= rrd::area('irq', '#ffc440', 'irq     ', true );
$def[1] .= rrd::gprint('irq', array('LAST', 'MIN', 'MAX', 'AVERAGE'), '%5.2lf %S' );

$def[1] .= rrd::area('softirq', '#ff40dc', 'softirq ', true );
$def[1] .= rrd::gprint('softirq', array('LAST', 'MIN', 'MAX', 'AVERAGE'), '%5.2lf %S' );

$def[1] .= rrd::area('idle', '#ffffff', 'idle    ', true );
$def[1] .= rrd::gprint('idle', array('LAST', 'MIN', 'MAX', 'AVERAGE'), '%5.2lf %S' );

# warning and critial thresholds not implemented in check yet
 
#if (isset($WARN[1]) &amp;&amp; $WARN[1] != "") {
#$def[1] .= "HRULE:$WARN[1]#FFFF00:\"Warning ($NAME[1])\: " . $WARN[1] . " " . $UNIT[1] . " \\n\" " ;
#}
#
#if (isset($CRIT[1]) &amp;&amp; $CRIT[1] != "") {
#$def[1] .= "HRULE:$CRIT[1]#FF0000:\"Critical ($NAME[1])\: " . $CRIT[1] . " " . $UNIT[1] . " \\n\" " ;
#}

?>
