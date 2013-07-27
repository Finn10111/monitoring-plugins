<?php

$defcnt = 1;

$colors['out'] = "#FF0000";
$colors['in'] = "#00FF00";

$colors['out_area'] = "#FF7F7F";
$colors['in_area'] = "#7FFF7F";

foreach ($DS as $i)
{
        if( $defcnt % 2 == 0 )
        {
                $defcntin = $defcnt-1;
                $ds_name[$defcnt] = "Traffic";

                $opt[$defcnt] = "--vertical-label \"Byte/s\" --title \"Traffic\" ";
                $def[$defcnt] = "";
                $def[$defcnt] .= rrd::hrule("0", "#888888");
                $def[$defcnt] .= rrd::def("out", $RRDFILE[$defcnt], $DS[$defcnt], "AVERAGE");
                $def[$defcnt] .= rrd::def("in", $RRDFILE[$defcntin], $DS[$defcntin], "AVERAGE");
                $def[$defcnt] .= rrd::cdef("out_neg", "out,-1,*");
                $def[$defcnt] .= rrd::area("out_neg", $colors['out_area']);
                $def[$defcnt] .= rrd::area("in", $colors['in_area']);
                $def[$defcnt] .= rrd::line1("in", $colors['in'], "in") ;
                $def[$defcnt] .= rrd::gprint("in", array("LAST", "MIN", "MAX", "AVERAGE"), "%4.2lf $UNIT[$defcntin]") ;
                $def[$defcnt] .= rrd::line1("out_neg", $colors['out'], "out") ;
                $def[$defcnt] .= rrd::gprint("out", array("LAST", "MIN", "MAX", "AVERAGE"), "%4.2lf $UNIT[$defcnt]") ;
        }
        $defcnt++;
}
?>

