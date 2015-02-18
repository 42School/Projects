import socket
from random import randint
import sys
import os
from math import sqrt

import Pyro4
from Pyro4.util import SerializerBase

from Tool import WorkClass


SerializerBase.register_dict_to_class("Tool.WorkClass", WorkClass.from_dict)
name = "Student_2014 #%d@%s" % (os.getpid(), socket.gethostname())
Awesome_quotes = []
Awesome_quotes.append(['Ready to work !', 'Ready to work..', 'The damned stand ready...', 'I stand ready'])




# Another try
# def factorize(n):
# factors = []
#     d = 2
#     while n > 1:
#         while n % d == 0:
#             factors.append(d)
#             n /= d
#         d = d + 1
#         if d*d > n:
#             if n > 1: factors.append(n)
#             break
#     return factors

# Lame algorithm !
# def factorize(n):
#     def isPrime(n):
#         return not any(x for x in xrange(2, int(sqrt(n)) + 1) if n % x == 0)
#
#     primes = []
#     candidates = xrange(2, n + 1)
#     candidate = 2
#     while not primes and candidate in candidates:
#         if candidate % 2 and n % candidate == 0 and isPrime(candidate):
#             primes = primes + [candidate] + factorize(n // candidate)
#         candidate += 1
#     return primes

def process(item):
    sys.stdout.flush()
    item.result = item.use()
    print(item.result)
    item.Handler = name

def main():
    dispatcher = Pyro4.core.Proxy("PYRONAME:PrimeFactoServ_42")
    print("Hello i'm slave %s" % name)
    print("Gotta get more work.")
    while True:
        try:
            item = dispatcher.getWork()
        except ValueError:
            print Awesome_quotes[0][randint(0, 3)]
        else:
            process(item)
            dispatcher.putResult(item)

if __name__ == "__main__":
    main()