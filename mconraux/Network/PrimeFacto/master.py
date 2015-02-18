import Queue

import Pyro4
from Pyro4.util import SerializerBase

from Tool import WorkClass


SerializerBase.register_dict_to_class("Tool.WorkClass", WorkClass.from_dict)


class MasterQueue(object):
    def __init__(self):
        self.work_queue = Queue.Queue()
        self.result_queue = Queue.Queue()

    def putWork(self, item):
        print 'before Putwork'
        self.work_queue.put(item)
        print 'after Putwork'

    def getWork(self, timeout=5):
        try:
            return self.work_queue.get(block=True, timeout=timeout)
        except Queue.Empty:
            raise ValueError("Empty Queue")

    def putResult(self, item):
        self.result_queue.put(item)

    def getResult(self, timeout=5):
        try:
            return self.result_queue.get(block=True, timeout=timeout)
        except Queue.Empty:
            raise ValueError("Result not found")

    def workQueueSize(self):
        return self.work_queue.qsize()

    def resultQueueSize(self):
        return self.result_queue.qsize()

# main program

Pyro4.Daemon.serveSimple({
    MasterQueue(): "PrimeFactoServ_42"
})
