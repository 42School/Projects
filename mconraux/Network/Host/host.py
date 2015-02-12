#!/usr/bin/python
"""Usage:
    host.py [-lvw] [--tcp] [-c CLASS] [-C | -t TYPE] [-W TIME | -w] [-G GTIME] <host>...
    host.py -h | --help | --version

Arguments:
    host                Hostname to check

Options:
    -h --help           Show this help message and exit
    --version           Show version and exit
    -v --verbose        Print verbose output
    -c CLASS            Specify class of the DNS request [default: IN]
    -C                  Attempt to display SOA records for from all the listed authoritative name servers.
    -t TYPE             Specify the type of request to make. Default is A, AAAA, and MX records.
    --tcp               Use TCP requests instead of UDP. TCP will be automatically selected for request that require it
    -W TIME             Timeout value for each query [default: 10]
    -G GTIME            Global timeout for cmd [default: 40]
    -w                  No timeout
    -l                  Attempt a zone transfer for zone <hostname>

"""


def formatA(answer):
    for elem in answer.rrset:
        print elem


def formatInfoVerb(tab):
    ret = []
    for strt in tab[:4]:
        index = strt.find(' ')
        ret.append(strt[:index] + ':' + strt[index:])
    print "[ " + ' | '.join(ret) + " ]\n"
    for strt in tab[4:]:
        if strt.startswith(';'):
            print str('--[+]' + strt[1:] + '[+]--').center(80,' ')
        else:
            ret = strt.split(' ')
            strt = "{:<{dyn}}".format(ret[0], dyn=40 if len(ret) == 3 else 30)
            if len(ret) == 5:
                strt += "{:<10}".format(ret.pop(1))
            strt += "{:<10}{:<10}".format(ret[1], ret[2])
            if len(ret) == 4:
                strt += ret[3]
            print strt


__author__ = 'Ep0ch'
# print __doc__
import dns.resolver
from docopt import docopt

arg = docopt(__doc__, version='0.1rc')
r = dns.resolver.Resolver()
# -- ASSIGN --
r.lifetime = float(arg['-G'])
r.timeout = float(arg['-W'])

types = []

if arg['-t']:
    types.append(arg['-t'])
else:
    types.append('A')
    types.append('AAAA')
    types.append('MX')
for type in types:
    for target in arg['<host>']:
        answer = r.query(target, type, arg['-c'], arg['--tcp'], raise_on_no_answer=False)
        # print 'RDType ',answer.rdtype
        # print 'QNAME ', answer.qname
        # print 'RDClass ', answer.rdclass
        if arg['--verbose']:
            print "=" * 80
            print "[*] Try for", target, 'with query', type, '[*]'
            formatInfoVerb(answer.response.__str__().splitlines())
        elif answer.rrset:
            formatA(answer)
        else:
            print target, 'has no', type, 'record'

# for rdata in r.query(sys.argv[1], sys.argv[2]):
#     print 'Host', rdata

