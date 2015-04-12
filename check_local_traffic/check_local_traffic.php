<?php
 
$defcnt = 1;
$defcntout = 1;
 
$colors['out'] = "#FF0000";
$colors['in'] = "#00FF00";
 
$colors['out_area'] = "#FF7F7F";
$colors['in_area'] = "#7FFF7F";
 
foreach ($DS as $i) 
{
	if( preg_match('/^bits_in_s$/', $NAME[$defcnt])) 
	{ 
		#$defcntin = $defcnt-1;
		$ds_name[$defcnt] = "Traffic";
 
		$opt[$defcnt] = "--vertical-label \"Bit/s\" --title \"Traffic\" ";
		$def[$defcnt] = "";
		$def[$defcnt] .= rrd::hrule("0", "#888888");
		$def[$defcnt] .= rrd::def("in", $RRDFILE[$defcnt], $DS[$defcnt], "AVERAGE"); 
		$def[$defcnt] .= rrd::area("in", $colors['in_area']);
		$def[$defcnt] .= rrd::line1("in", $colors['in'], "in") ;
                $def[$defcnt] .= rrd::gprint("in", array("LAST", "MIN", "MAX", "AVERAGE"), "%4.2lf %s");
                if ( isset($WARN[$defcnt]) )
                {
                    $def[$defcnt] .= rrd::hrule($WARN[$defcnt], "#FFFF00");
                }
                if ( isset($CRIT[$defcnt]) )
                {
                    $def[$defcnt] .= rrd::hrule($CRIT[$defcnt], "#FF0000");
                }
		
		$defcntout = 1;
		foreach ($DS as $j)
		{
			if( preg_match('/^bits_out_s$/', $NAME[$defcntout]) ) 
			{
				$def[$defcnt] .= rrd::def("out", $RRDFILE[$defcntout], $DS[$defcntout], "AVERAGE"); 
				$def[$defcnt] .= rrd::cdef("out_neg", "out,-1,*");
				$def[$defcnt] .= rrd::area("out_neg", $colors['out_area']);
                                $def[$defcnt] .= rrd::line1("out_neg", $colors['out'], "out") ;
                                $def[$defcnt] .= rrd::gprint("out", array("LAST", "MIN", "MAX", "AVERAGE"), "%4.2lf %s");
                                if ( isset($WARN[$defcnt]) )
                                {
                                    $def[$defcnt] .= rrd::hrule($WARN[$defcnt]*-1, "#FFFF00");
                                }
                                if ( isset($CRIT[$defcnt]) )
                                {
                                    $def[$defcnt] .= rrd::hrule($CRIT[$defcnt]*-1, "#FF0000");
                                }
			}
        		$defcntout++;
		}
    	}

        $defcnt++;
}
?>
