#!/usr/bin/env python
import sys
import re
import subprocess
import argparse

class NetstatCurrent:
    __tcp_conns = 0
    __tcp_conns_established = 0
    __tcp_conns_syn_sent = 0
    __tcp_conns_syn_recv = 0
    __tcp_conns_fin_wait1 = 0
    __tcp_conns_fin_wait2 = 0
    __tcp_conns_time_wait = 0
    __tcp_conns_close = 0
    __tcp_conns_close_wait = 0
    __tcp_conns_last_ack = 0
    __tcp_conns_listen = 0
    __tcp_conns_closing = 0
    __tcp_conns_unknown = 0
    __udp_conns = 0
    __warning = False
    __critical = False

    def __init__(self, warning=False, critical=False):
        self.__warning = int(warning)
        self.__critical = int(critical)

    def run(self):
        return self.__call_netstat__()

    def __call_netstat__(self):
        netstat_output = subprocess.Popen('LANG=en_EN.utf8 netstat -antu | tail -n +3', shell=True,
                stdout=subprocess.PIPE).communicate()[0]
        return self.__process_netstat_output__(netstat_output)

    def __exit__(self):
        sum_conns = self.__tcp_conns + self.__udp_conns
        return_code = 0
        if sum_conns >= self.__critical:
            return_code = 2
            prefix = 'CRITICAL:'
        elif sum_conns >= self.__warning:
            return_code = 1
            prefix = 'WARNING:'
        else:
            return_code = 0
            prefix = 'OK:'
                
        
        values = {'prefix' : prefix, 'sum_conns' : sum_conns,
                'tcp_conns' : self.__tcp_conns, 'udp_conns' : self.__udp_conns, 
                'warning' : self.__warning, 'critical' : self.__critical}
        output = '%(prefix)s Total Connections: \
%(sum_conns)s, \
TCP Connections: %(tcp_conns)s, UDP Connections: %(udp_conns)s \
| total_conns=%(sum_conns)s;%(warning)s;%(critical)s tcp_conns=%(tcp_conns)s \
udp_conns=%(udp_conns)s' % values

        print output
        return return_code


    def __process_netstat_output__(self, netstat_output):
        netstat_list = netstat_output.split('\n')
        for line in netstat_list:
            tmp = re.split('\s*', line)
            if re.match('tcp', tmp[0]):
                self.__tcp_conns += 1
                if re.match('ESTABLISHED', tmp[5]):
                    self.__tcp_conns_established += 1
                elif re.match('SYN_SENT', tmp[5]):
                    self.__tcp_conns_syn_sent += 1
                elif re.match('SYN_RECV', tmp[5]):
                    self.__tcp_conns_syn_recv += 1
                elif re.match('FIN_WAIT1', tmp[5]):
                    self.__tcp_conns_fin_wait1 += 1
                elif re.match('FIN_WAIT2', tmp[5]):
                    self.__tcp_conns_fin_wait2 += 1
                elif re.match('TIME_WAIT', tmp[5]):
                    self.__tcp_conns_time_wait += 1
                elif re.match('CLOSE', tmp[5]):
                    self.__tcp_conns_close += 1
                elif re.match('CLOSE_WAIT', tmp[5]):
                    self.__tcp_conns_close_wait += 1
                elif re.match('LAST_ACK', tmp[5]):
                    self.__tcp_conns_last_ack += 1
                elif re.match('LISTEN', tmp[5]):
                    self.__tcp_conns_listen += 1
                elif re.match('CLOSING', tmp[5]):
                    self.__tcp_conns_closing += 1
                elif re.match('UNKNOWN', tmp[5]):
                    self.__tcp_conns_unknown += 1
            elif re.match('udp', tmp[0]):
                self.__udp_conns += 1

        return self.__exit__()


def main():
    parser = argparse.ArgumentParser(description = 'Nagios plugin to check netstat statistics')
    thresholds = parser.add_argument_group('thresholds', 'warning and critical thresholds for total number of connections')
    thresholds.add_argument('-w', '--warning', required=False, default=False,
            type=int)
    thresholds.add_argument('-c', '--critical', required=False, default=False,
            type=int)
    args = parser.parse_args()

    netstat_current = NetstatCurrent(args.warning, args.critical)
    return netstat_current.run()


if __name__ == '__main__':
    sys.exit(main())

