#!/usr/bin/python
"""Usage:
    host.py [-lgivqw] [--tcp] [-c CLASS] [-t TYPE] [-W TIME] [-G GTIME] <host>...
    host.py -h | --help | --version

Arguments:
    host                Hostname to check

Options:
    -h --help           Show this help message and exit
    --version           Show version and exit
    -v --verbose        Print verbose output
    -q --quiet          Print less output
    -c CLASS            Specify class of the DNS request [default: IN]
    -i                  Use IP6.INT instead of IP6.ARPA for reversing IPv6 addresses
    -t TYPE             Specify the type of request to make. Default is A, AAAA, and MX records.
    --tcp               Use TCP requests instead of UDP. TCP will be automatically selected for request that require it
    -W TIME             Timeout value for each query [default: 10]
    -G GTIME            Global timeout for cmd [default: 30]
    -l                  Attempt a zone transfer for zone <hostname>

"""

from dns import resolver, reversename, name
from docopt import docopt
import re
__author__ = 'Ep0ch'

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


arg = docopt(__doc__, version='0.2rc')
r = resolver.Resolver()
# -- ASSIGN --

r.lifetime = float(arg['-G'])
r.timeout = float(arg['-W'])
ip_checker = re.compile('(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))')


for target in arg['<host>']:
    if arg['-t']:
        types = [arg['-t']]
    elif ip_checker.match(target): #Absolute IP
        target = reversename.from_address(target)
        if arg['-i']:
            target = name.from_text(target.__str__()[:-5] + 'int')
        print target
        types = ['PTR']
    else:
        types = ['A', 'AAAA', 'MX']
    for type in types:
        try:
            answer = r.query(target, type, arg['-c'], arg['--tcp'], raise_on_no_answer=False)
        except resolver.NXDOMAIN:
            print "Invalid request"
            exit()
        except resolver.Timeout:
            print "Didn't found any answers in required time"
            exit()
        if arg['--verbose']:
            print "=" * 80
            print "[*] Try for", target, 'with query', type, '[*]'
            formatInfoVerb(answer.response.__str__().splitlines())
        elif answer.rrset:
            for ret in answer.rrset:
                print target, 'has', type, 'record', ret
        else:
            print target, 'has no', type, 'record'
