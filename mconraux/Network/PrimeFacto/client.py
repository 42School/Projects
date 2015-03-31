import random
import sys

import Pyro4
from Pyro4.util import SerializerBase

from Tool import WorkClass


SerializerBase.register_dict_to_class("Tool.WorkClass", WorkClass.from_dict)

items_number = int(raw_input("How much to compute ? : "))
if len(sys.argv) >= 2 and sys.argv[1] == '-q':
    quiet = True
else:
    quiet = False


def launch():
    print("\nThis program will send and activate WorkClass units to slaves. Current algo is : PrimeFactorials")
    with Pyro4.core.Proxy("PYRONAME:PrimeFactoServ_42") as master:
        place_work(master)
        numbers =  collect_results(master).items()
    numbers.sort()
    print_result(numbers)


def place_work(master):
    print("placing work instances into master queue.")
    print items_number
    for i in xrange(items_number):
        print i
        number = random.randint(3211, 100000) * random.randint(3211, 100000)
        item = WorkClass(i + 1, number)
        master.putWork(item)


def collect_results(master):
    print("getting results from master queue.")
    numbers = {}
    while len(numbers) < items_number:
        try:
            item = master.getResult()
        except ValueError:
            print("Not all results available (got %d out of %d). Work queue size: %d" %
                  (len(numbers), items_number, master.workQueueSize()))
        else:
            if not quiet: print("Got result: %s (from %s)" % (item, item.Handler))
            numbers[item.data] = item.result

    if master.resultQueueSize() > 0:
        print "You shouldn't be here."
        numbers += collect_results(master)
    return numbers


def print_result(numbers):
    print("\nComputed Results:")
    for (number, factorials) in numbers:
        print "%s %d <-> %s" % ("{:<5}".format('['+str(len(factorials))+']'),number, factorials)


if __name__ == '__main__':
    launch()