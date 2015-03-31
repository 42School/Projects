import socket
from random import randint
import sys
import os

import Pyro4
from Pyro4.util import SerializerBase

from Tool import WorkClass


SerializerBase.register_dict_to_class("Tool.WorkClass", WorkClass.from_dict)
name = "Student_2014 #%d@%s" % (os.getpid(), socket.gethostname())
Awesome_quotes = []
Awesome_quotes.append(['Ready to work !', 'Ready to work..', 'The damned stand ready...', 'I stand ready'])



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