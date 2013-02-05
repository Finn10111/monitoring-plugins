#!/usr/bin/python2

import sys
import re
from pynag.Plugins import PluginHelper,ok,warning,critical,unknown

def main():
        helper = PluginHelper()

        helper.parser.add_option('-w', help='warning free (X% or XM)', dest='warning')
        helper.parser.add_option('-c', help='critical free (X% or XM)', dest='critical')
        helper.parse_arguments()
        warn = helper.options.warning
        crit = helper.options.critical

	memory = getMemory()
	
        
	if helper.options.warning is not None:
		warn = helper.options.warning
		if re.match('.*%$', warn):
			warn = str(memory['total'] * int(re.search('\d*', warn).group(0)) / 100)
	else: 
		warn = '0'
	 
	if helper.options.critical is not None:
		crit = helper.options.critical
		if re.match('.*%$', crit):
			crit = str(memory['total'] * int(re.search('\d*', crit).group(0)) / 100)
	else: 
		crit = '0'

        helper.status(ok)
	status = "OK"
        
	if memory['totalfree'] <= int(warn):
		helper.status(warning)
		status = "WARNING"

	if memory['totalfree'] <= int(crit):
		helper.status(critical)
		status = "CRITICAL"

	helper.add_summary(status + ': Memory free: %(totalfree)s %% (%(free)s %% including buffers/cached)' % {'totalfree': (round((float(memory['totalfree']) / float(memory['total']) * 100), 1 )), 'free': (round((float(memory['free']) / float(memory['total']) * 100), 1 ))})
        helper.add_metric(label='total',value=memory['total'])
        helper.add_metric(label='free',value=memory['free'])
        helper.add_metric(label='totalfree',value=memory['totalfree'], warn=warn+'..0', crit=crit+'..0')
        helper.add_metric(label='used',value=memory['used'])
        helper.add_metric(label='buffers',value=memory['buffers'])
        helper.add_metric(label='cached',value=memory['cached'])
        helper.add_metric(label='swapcached',value=memory['swapcached'])


	helper.check_all_metrics()
        helper.exit()


def getMemory():
        try:
		memory = open('/proc/meminfo').read()
		total = int(re.search('(MemTotal:)(\s*)(\d*)', memory, re.M).group(3)) * 1000 
		free = int(re.search('(MemFree:)(\s*)(\d*)', memory, re.M).group(3)) * 1000 
		buffers = int(re.search('(Buffers:)(\s*)(\d*)', memory, re.M).group(3)) * 1000 
		cached = int(re.search('(Cached:)(\s*)(\d*)', memory, re.M).group(3)) * 1000 
		swapcached = int(re.search('(SwapCached:)(\s*)(\d*)', memory, re.M).group(3)) * 1000
		used = total - free - buffers - cached
		totalfree = total - used 
        except Exception, e:
                helper.exit(summary='Could not read /proc/meminfo', long_output=str(e), exit_code=unknown, perfdata='')
	
	return dict({'total': total, 'used': used ,'free': free, 'totalfree': totalfree, 'buffers': buffers, 'cached': cached, 'swapcached': swapcached})


if __name__ == '__main__':
        sys.exit(main())

